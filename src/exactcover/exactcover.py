"""Exactcover finds all solutions to an exact cover problem."""


from copy import deepcopy
from random import shuffle
from typing import Any, Dict, Hashable, List, Optional, Tuple, Union


def solve(universe_columns: Union[Dict[Hashable, Any], List[Hashable], set, str,
                                  Tuple[Hashable]],
          subsets_rows: Dict[Hashable, set],
          limit: Optional[int] = None, randomize: bool = False,
          preseed: Optional[set] = None, count: bool = False) -> List[set]:
    """Solves exact cover problems.

    Given the set universe_columns and collection of subsets, the function finds all solutions to
    the exact cover problem.

    Args:
        universe_columns:
            The set of elements in the universe/columns. Duplicate elements are silently ignored.
        subsets_rows:
            The collection of subsets in `universe_columns` of type dict.  The values are python
            set objects that is a subset of `universe_columns`.
        limit:
            A positive integer. The number of solutions returned is <= `limit`. This option is
            ignored if the value is not a positive integer. Default: `None`
        randomize:
            When `true`, solutions are returned in random order. This option is ignored if the
            value is not a boolean. Default: `False`
        preseed:
            A set of hashable row objects used to preseed a partial solution. This option is
            ignored if the value is not a set object. Default: `None`
        count:
            When `True`, the total number of solutions is returned instead of the solution sets.
            The `limit` and `randomize` options are ignonred when `count` is set to `True`. This
            option is ignored if the value is not a boolean. Defaut: `False`

    Returns:
        List[set]: A list of solutions.
    """

    def _reduce_and_update(row, sr_backtrack, uc_backtrack):
        for co_uc_idx in SR[row]:
            if co_uc_idx not in UC:
                # contradiction
                return False
            for co_sr_idx in UC[co_uc_idx]:
                if co_sr_idx in sr_backtrack:
                    continue
                sr_backtrack[co_sr_idx] = set()
                for other_uc_idx in SR[co_sr_idx]:
                    if other_uc_idx not in SR[row]:
                        sr_backtrack[co_sr_idx].add(other_uc_idx)
                        del UC[other_uc_idx][co_sr_idx]
            uc_backtrack[co_uc_idx] = UC[co_uc_idx]
            del UC[co_uc_idx]
        partial.add(row)

    def _solve():
        nonlocal results
        if not UC:
            # Solution was found
            if not _count:
                results.append(partial.copy())
            else:
                results += 1
            return True

        selected_uc = min(UC, key=lambda x: len(UC[x]))
        if not UC[selected_uc]:
            # There is no solution if this universe element is not covered by any subset
            return False

        for selected_row_idx in UC[selected_uc]:
            uc_backtrack = {}
            sr_backtrack = {}
            _reduce_and_update(selected_row_idx,
                               sr_backtrack,
                               uc_backtrack)

            if _solve() and _limit is not None and (
                    (_count is True and results >= _limit) or
                    (_count is False and len(results) >= _limit)
            ):
                return True

            # Backtrack: Restore cols & rows; Remove row from partial solution
            for co_uc_key in uc_backtrack:
                UC[co_uc_key] = uc_backtrack[co_uc_key]
            for co_sr_idx in sr_backtrack:
                for other_uc_idx in sr_backtrack[co_sr_idx]:
                    UC[other_uc_idx][co_sr_idx] = None
            partial.remove(selected_row_idx)
        return False

    def _initialize_sets():
        nonlocal SR
        if _randomize is True:
            tmp_sr_idx = list(subsets_rows)
            shuffle(tmp_sr_idx)
            for i in tmp_sr_idx:
                SR[i] = deepcopy(subsets_rows[i])
        else:
            SR = deepcopy(subsets_rows)
        for u_element in universe_columns:
            UC[u_element] = {}
        for s_key, u_subset in SR.items():
            # Add row cross-reference for each universe element
            for u_key in u_subset:
                if u_key not in UC:
                    raise ExactCoverKeyError('BadUKey', (u_key, s_key))
                UC[u_key][s_key] = None

    def _make_limit():
        if isinstance(limit, int):
            if limit > 0:
                return limit
        return None

    def _check_preseed():
        if isinstance(preseed, set):
            for r in preseed:
                if r not in SR:
                    raise ExactCoverKeyError('BadPreseed', r)
            return deepcopy(preseed)
        return set()

    def _do_preseed():
        while len(_preseed) > 0:
            row = _preseed.pop()
            sr_backtrack = {}
            uc_backtrack = {}
            if _reduce_and_update(row, sr_backtrack, uc_backtrack) is False:
                return False

    def _check_count():
        if count is True:
            return True
        return False

    partial = set()
    UC = {}
    SR = {}
    _randomize = True if randomize is True else False
    _initialize_sets()
    _count = _check_count()
    results = [] if not _count else 0
    _limit = _make_limit()
    _preseed = _check_preseed()
    if _do_preseed() is False:
        return results
    _solve()
    return results


class ExactCoverKeyError(Exception):
    """Key error exception with descriptive messages.

    An `exactcover.ExactCoverKeyError` exception is raised when a subset in `subset_rows` contains
    an element that is not in `universe_columns`, or a preseed set contains an element that is not
    in `subsets_rows`.
    """

    def __init__(self, *args):
        """Set the message."""
        self.num = args[0]
        self.keys = args[1]
        if self.num == 'BadPreseed':
            self.msg = (f'ExactCoverKeyError: Element {repr(self.keys)} in '
                        f'preseed is not in subsets_rows')
        if self.num == 'BadUKey':
            self.msg = (f'ExactCoverKeyError: Element {repr(self.keys[0])} in '
                        f'subsets_rows {repr(self.keys[1])} is not in '
                        f'Universe')

    def __str__(self):
        """Return the message string."""
        return self.msg


if __name__ == '__main__':
    pass
