"""Tests for the exactcover module."""
import pytest
from exactcover.exactcover import solve, ExactCoverKeyError


@pytest.fixture
def trivial():
    return {'u': {0}, 's': {0: {0}}}


@pytest.fixture
def example():
    return {
        'u': {1, 2, 3, 4, 5, 6, 7},
        's': {
            'A': {1, 4, 7},
            'B': {1, 4},
            'C': {4, 5, 7},
            'D': {3, 5, 6},
            'E': {2, 3, 6, 7},
            'F': {2, 7},
            }
    }


@pytest.fixture
def small_example():
    return {
        'u': {1, 2, 3, 4},
        's': {
            'A': {1, 2},
            'B': {3, 4},
            'C': {2, 4},
            'D': {1, 3},
            }
    }


def test_returns_set():
    assert isinstance(solve(set(), dict()), list)


def test_accept_set_u(trivial):
    assert isinstance(solve(trivial['u'], trivial['s']), list)


def test_accept_list_u(trivial):
    assert isinstance(solve(list(trivial['u']), trivial['s']), list)


def test_accept_dict_u(trivial):
    assert isinstance(solve({x: x for x in trivial['u']}, trivial['s']), list)


def test_accept_tuple_u(trivial):
    assert isinstance(solve(tuple(trivial['u']), trivial['s']), list)


def test_accept_str_u(trivial):
    s = {k: set([str(x) for x in v]) for k, v in trivial['s'].items()}
    assert isinstance(solve(''.join(map(str, trivial['u'])), s), list)


def test_example(example):
    assert [{'B', 'D', 'F'}] == solve(example['u'], example['s'])


def test_no_solution(example):
    example['s']['D'].remove(6)
    example['s']['E'].remove(6)
    assert [] == solve(example['u'], example['s'])


def test_srow_contains_element_not_in_u(example):
    extra = 10
    subset = 'B'
    example['s'][subset].add(extra)
    with pytest.raises(ExactCoverKeyError) as e:
        solve(example['u'], example['s'])
    assert (f'ExactCoverKeyError: Element {repr(extra)} in '
            f'subsets_rows {repr(subset)} is not in Universe') == str(e.value)


def test_s_contains_empty_srow(example):
    example['s']['G'] = set()
    assert [{'B', 'D', 'F'}] == solve(example['u'], example['s'])


def test_solution_in_single_srow(example):
    example['s']['A'] = set()
    example['s']['B'] = {1, 2, 3, 4, 5, 6, 7}
    example['s']['C'] = set()
    example['s']['D'] = set()
    example['s']['E'] = set()
    example['s']['F'] = set()
    assert [{'B'}] == solve(example['u'], example['s'])


def test_one_each_in_subset():
    u = {1, 2, 3}
    s = {10: {2}, 20: {1}, 30: {3}}
    assert [{10, 20, 30}] == solve(u, s)


def test_duplicate_subset_not_in_solution(example):
    example['s']['G'] = {1, 4, 7}
    assert [{'B', 'D', 'F'}] == solve(example['u'], example['s'])


def test_multiple_solutions_all_results_default(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'])
    assert [{'B', 'D', 'F'}, {'B', 'F', 'G'}] == result


def test_limit_empty_inputs():
    assert isinstance(solve(set(), dict(), limit=1), list)


def test_limit1_multiple_solutions(example):
    example['s']['G'] = {3, 5, 6}
    assert [{'B', 'D', 'F'}] == solve(example['u'], example['s'], limit=1)


def test_limiteqall_multiple_solutions(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'], limit=2)
    assert [{'B', 'D', 'F'}, {'B', 'F', 'G'}] == result


def test_limitgtall_multiple_solutions(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'], limit=3)
    assert [{'B', 'D', 'F'}, {'B', 'F', 'G'}] == result


def test_limit0_multiple_solutions(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'], limit=0)
    assert [{'B', 'D', 'F'}, {'B', 'G', 'F'}] == result


def test_limitneg1_multiple_solutions(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'], limit=-1)
    assert [{'B', 'D', 'F'}, {'B', 'G', 'F'}] == result


def test_invalid_limit_multiple_solutions(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'], limit='a')
    assert [{'B', 'D', 'F'}, {'B', 'F', 'G'}] == result


def test_limit1_random_multiple_solutions(small_example):
    counts_ab = 0
    counts_cd = 0
    size = 100
    for i in range(size):
        result = solve(small_example['u'], small_example['s'],
                       limit=1, randomize=True)
        if [{'A', 'B'}] == result:
            counts_ab += 1
        if [{'C', 'D'}] == result:
            counts_cd += 1
    assert counts_ab != 0 and counts_cd != 0


def test_limit1_nonrandom_multiple_solutions(small_example):
    size = 100
    counts = {}
    for i in range(size):
        result = tuple(sorted(list(solve(small_example['u'], small_example['s'],
                                         limit=1, randomize=False).pop())))
        if result not in counts:
            counts[result] = 1
        else:
            counts[result] += 1
    assert len(counts) == 1 and counts[result] == size


def test_preseed_empty(example):
    assert [{'B', 'D', 'F'}] == solve(example['u'], example['s'], preseed={})


def test_preseed_ignores_wrong_type_empty(example):
    assert [{'B', 'D', 'F'}] == solve(example['u'], example['s'], preseed=[])


def test_preseed_ignores_wrong_type(example):
    assert [{'B', 'D', 'F'}] == solve(example['u'], example['s'], preseed=[1])


def test_preseed_contains_1x_correct(example):
    result = solve(example['u'], example['s'], preseed={'B'})
    assert [{'B', 'D', 'F'}] == result


def test_preseed_contains_2x_correct(example):
    result = solve(example['u'], example['s'], preseed={'B', 'F'})
    assert [{'B', 'D', 'F'}] == result


def test_preseed_contains_all_correct(example):
    result = solve(example['u'], example['s'], preseed={'B', 'D', 'F'})
    assert [{'B', 'D', 'F'}] == result


def test_preseed_contains_all_correct_and_1x_incorrect(example):
    result = solve(example['u'], example['s'], preseed={'B', 'D', 'F', 'C'})
    assert [] == result


def test_preseed_contains_incorrect(example):
    assert [] == solve(example['u'], example['s'], preseed={'A'})


def test_preseed_contains_mix_incorrect_correct(example):
    assert [] == solve(example['u'], example['s'], preseed={'A', 'B'})


def test_preseed_contains_invalid(example):
    fill = 'G'
    with pytest.raises(ExactCoverKeyError) as e:
        solve(example['u'], example['s'], preseed={fill})
    assert (f'ExactCoverKeyError: Element {repr(fill)} in preseed '
            f'is not in subsets_rows') == str(e.value)


def test_preseed_contains_mix_invalid_correct(example):
    fill = 'G'
    with pytest.raises(ExactCoverKeyError) as e:
        solve(example['u'], example['s'], preseed={fill, 'B'})
    assert (f'ExactCoverKeyError: Element {repr(fill)} in preseed '
            f'is not in subsets_rows') == str(e.value)


def test_preseed_multiple_solutions_choose_correct_possibility(example):
    example['s']['G'] = {3, 5, 6}
    result_d = solve(example['u'], example['s'], limit=1, preseed={'D'})
    result_g = solve(example['u'], example['s'], limit=1, preseed={'G'})
    assert [{'B', 'D', 'F'}] == result_d
    assert [{'B', 'F', 'G'}] == result_g


def test_preseed_multiple_solutions_choose_incorrect_possibility(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'], limit=1, preseed={'C'})
    assert [] == result


def test_count_one_solution(example):
    assert 1 == solve(example['u'], example['s'], count=True)


def test_count_no_solution(example):
    example['s']['D'].remove(6)
    example['s']['E'].remove(6)
    assert 0 == solve(example['u'], example['s'], count=True)


def test_count_multiple_solutions(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'], count=True)
    assert 2 == result


def test_count_false(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'], count=False)
    assert [{'B', 'D', 'F'}, {'B', 'F', 'G'}] == result


def test_count_ignore(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'], count=3)
    assert [{'B', 'D', 'F'}, {'B', 'F', 'G'}] == result


def test_count_preseed_2solutionTo2count(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'], preseed={'B'}, count=True)
    assert 2 == result


def test_count_preseed_2solutionTo1count(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'], preseed={'D'}, count=True)
    assert 1 == result


def test_count_preseed_2solutionTo0count(example):
    example['s']['G'] = {3, 5, 6}
    result = solve(example['u'], example['s'], preseed={'A'}, count=True)
    assert 0 == result
