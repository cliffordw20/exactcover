"""Examples for exactcover."""
from exactcover.exactcover import solve


# Basic usage
u = {1, 2, 3, 4, 5, 6, 7}
s = {
    'A': {1, 4, 7},
    'B': {1, 4},
    'C': {4, 5, 7},
    'D': {3, 5, 6},
    'E': {2, 3, 6, 7},
    'F': {2, 7},
}
result = solve(u, s)
print(result)
# [{'D', 'F', 'B'}]


# An example with multiple solutions.
u = {1, 2, 3, 4, 5, 6, 7}
s = {
    'A': {1, 4, 7},
    'B': {1, 4},
    'C': {4, 5, 7},
    'D': {3, 5, 6},
    'E': {2, 3, 6, 7},
    'F': {2, 7},
    'G': {3, 5, 6},
}
result = solve(u, s)
print(result)
# [{'D', 'F', 'B'}, {'G', 'F', 'B'}]


# No solution
u = {1, 2, 3, 4, 5, 6, 7}
s = {
    'A': {1, 4, 7},
    'B': {1, 4},
    'C': {4, 5, 7},
    'D': {3, 5},
    'E': {2, 3, 7},
    'F': {2, 7},
}
result = solve(u, s)
print(result)
# []


# universe_columns as a string.
u = '1234567'
s = {
    'A': {'1', '4', '7'},
    'B': {'1', '4'},
    'C': {'4', '5', '7'},
    'D': {'3', '5', '6'},
    'E': {'2', '3', '6', '7'},
    'F': {'2', '7'},
    'G': {'3', '5', '6'},
}
result = solve(u, s)
print(result)
# [{'D', 'F', 'B'}, {'G', 'F', 'B'}]


# By default, the order of the results is not random.
u = {1, 2, 3, 4, 5, 6, 7}
s = {
    'A': {1, 4, 7},
    'B': {1, 4},
    'C': {4, 5, 7},
    'D': {3, 5, 6},
    'E': {2, 3, 6, 7},
    'F': {2, 7},
    'G': {3, 5, 6},
}
result = solve(u, s, limit=1)
print(result)
# [{'D', 'F', 'B'}]
result = solve(u, s, limit=1)  # Solving the problem again yields the same result.
print(result)
# [{'D', 'F', 'B'}]
# Use randomize=True to randomize the order. This option is useful to get a
# random solution from a problem that has multiple solutions.
for i in range(10):
    result = solve(u, s, limit=1, randomize=True)
    print(result)
# [{'G', 'F', 'B'}]
# [{'G', 'F', 'B'}]
# [{'D', 'F', 'B'}]
# [{'D', 'F', 'B'}]
# [{'D', 'F', 'B'}]
# [{'D', 'F', 'B'}]
# [{'G', 'F', 'B'}]
# [{'D', 'F', 'B'}]
# [{'G', 'F', 'B'}]
# [{'G', 'F', 'B'}]


# Use preseed to populate a partial solution set.
# This problem has four solutions.
u = {1, 2, 3, 4, 5, 6, 7}
s = {
    'A': {1, 4, 7},
    'B': {1, 4},
    'C': {4, 5, 7},
    'D': {3, 5, 6},
    'E': {2, 3, 6, 7},
    'F': {2, 7},
    'G': {3, 5, 6},
    'H': {1, 4},
}
result = solve(u, s, preseed={'B'})  # What is the result when 'B' is chosen?
print(result)
# [{'D', 'F', 'B'}, {'G', 'F', 'B'}]
result = solve(u, s, preseed={'D'})  # What is the result when 'D' is chosen?
print(result)
# [{'D', 'F', 'B'}, {'H', 'D', 'F'}]
result = solve(u, s, preseed={'B', 'G'})  # What is the result when 'B' and 'G' is chosen?
print(result)
# [{'G', 'F', 'B'}]
result = solve(u, s, preseed={'A'})  # What is the result when 'A' is chosen?
print(result)
# []


# Count the number of solutions
u = {1, 2, 3, 4, 5, 6, 7}
s = {
    'A': {1, 4, 7},
    'B': {1, 4},
    'C': {4, 5, 7},
    'D': {3, 5, 6},
    'E': {2, 3, 6, 7},
    'F': {2, 7},
    'G': {3, 5, 6},
    'H': {1, 4},
}
result = solve(u, s, count=True)
print(result)
# 4


# Use limit to determine if there is a certain number of solutions.
# In this example, we ask if there is at least two solutions.
u = {1, 2, 3, 4, 5, 6, 7}
s = {
    'A': {1, 4, 7},
    'B': {1, 4},
    'C': {4, 5, 7},
    'D': {3, 5, 6},
    'E': {2, 3, 6, 7},
    'F': {2, 7},
    'G': {3, 5, 6},
    'H': {1, 4},
}
result = solve(u, s, count=True, limit=2)
print(result)
# 2
