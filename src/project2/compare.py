import timeit

# Importing the solve functions from the three Python files
from backtrack import solve as solve_backtrack
from brute_force import solve as solve_bruteforce
from pysat_solver import solve as solve_pysat

# Define setup code if necessary
setup_code = """
from __main__ import solve_backtrack, solve_bruteforce, solve_pysat
"""

# Measure the execution time for each function
time_backtrack = timeit.timeit(stmt="solve_backtrack()", setup=setup_code, number=1)
time_bruteforce = timeit.timeit(stmt="solve_bruteforce()", setup=setup_code, number=1)
time_pysat = timeit.timeit(stmt="solve_pysat()", setup=setup_code, number=1)

# Print the execution time for each function
print("Execution time for solve() function in backtrack.py:", time_backtrack)
print("Execution time for solve() function in brute_force.py:", time_bruteforce)
print("Execution time for solve() function in pysat_solver.py:", time_pysat)