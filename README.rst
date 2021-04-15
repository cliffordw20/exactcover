
Overview
********

Exactcover is a solver that finds all solutions to an exact cover
problem. The *solve* function accepts multple input types and returns
a list of solution sets.

Features:

*  Find all solutions

*  An option to limit the number of solutions

*  An option to randomize the solution list

*  An option to pre-select rows before solving

*  An option to return the number of solutions instead of solution
   sets


Exactcover
**********

Exactcover finds all solutions to an exact cover problem.

**exactcover.exactcover.solve(universe_columns, subsets_rows,
limit=None, randomize=False, preseed=None, count=False)**

   Solves exact cover problems.

   Given the set universe_columns and collection of subsets, the
   function finds all solutions to the exact cover problem.

   :Parameters:
      *  **universe_columns** (*Union[Dict[Hashable, Any],
         List[Hashable], set, str, Tuple[Hashable]]*) – The set of
         elements in the universe/columns. Duplicate elements are
         silently ignored.

      *  **subsets_rows** (*Dict[Hashable, set]*) – The collection of
         subsets in *universe_columns* of type dict.  The values are
         python set objects that is a subset of *universe_columns*.

      *  **limit** (*Optional[int]*) – A positive integer. The number
         of solutions returned is <= *limit*. This option is ignored
         if the value is not a positive integer. Default: *None*

      *  **randomize** (*bool*) – When *true*, solutions are returned
         in random order. This option is ignored if the value is not a
         boolean. Default: *False*

      *  **preseed** (*Optional[set]*) – A set of hashable row objects
         used to preseed a partial solution. This option is ignored if
         the value is not a set object. Default: *None*

      *  **count** (*bool*) – When *True*, the total number of
         solutions is returned instead of the solution sets. The
         *limit* and *randomize* options are ignonred when *count* is
         set to *True*. This option is ignored if the value is not a
         boolean. Defaut: *False*

   :Returns:
      *List[set]* – A list of solutions.

   :Return type:
      List[set]

**exception exactcover.exactcover.ExactCoverKeyError(*args)**

   Key error exception with descriptive messages.

   An *exactcover.ExactCoverKeyError* exception is raised when a
   subset in *subset_rows* contains an element that is not in
   *universe_columns*, or a preseed set contains an element that is
   not in *subsets_rows*.


Examples
********

.. code::

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
