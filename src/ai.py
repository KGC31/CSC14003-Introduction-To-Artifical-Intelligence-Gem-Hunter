from itertools import combinations
from pysat.solvers import Solver

# Example grid with clues provided
grid = [
    [3, '_', 2, '_'],
    ['_', '_', 2, '_'],
    ['_', 3, 1, '_'],
]

# Assign logical variables to each cell
logical_vars = {}
var_counter = 1
for r in range(len(grid)):
    for c in range(len(grid[r])):
        logical_vars[(r, c)] = var_counter
        var_counter += 1

# Function to find neighboring cells around a given cell
def find_neighbors(row, col, grid):
    neighbors = []
    for r in range(max(0, row - 1), min(len(grid), row + 2)):
        for c in range(max(0, col - 1), min(len(grid[0]), col + 2)):
            if (r, c) != (row, col):
                neighbors.append((r, c))
    return neighbors

# Generate CNF clauses based on the grid clues
cnf_clauses = []
for r in range(len(grid)):
    for c in range(len(grid[r])):
        if isinstance(grid[r][c], int):  # If the cell contains a numerical clue
            clue_number = grid[r][c]
            neighbors = find_neighbors(r, c, grid)
            neighbor_vars = [logical_vars[neighbor] for neighbor in neighbors]
            
            # Generate combinations of neighbors that fulfill the clue's number of traps
            positive_combinations = list(combinations(neighbor_vars, clue_number))
            
            # Generate clauses that meet the clue requirement
            if positive_combinations:
                clause_set = []
                for combo in positive_combinations:
                    positive_clause = list(combo)
                    negative_clause = [-v for v in neighbor_vars if v not in combo]
                    clause_set.append(positive_clause + negative_clause)

                # Add the clause set to the CNF clauses
                cnf_clauses.extend(clause_set)
                print(f"Adding clauses for cell ({r},{c}) with clue {clue_number}: {clause_set}")

# Initialize the SAT solver
solver = Solver(name='g3')

# Add generated CNF clauses to the solver
for clause in cnf_clauses:
    solver.add_clause(clause)

# Solve the problem using the solver
if solver.solve():
    solution = solver.get_model()
    print("Solution found:", solution)

    # Map logical variables back to grid positions and traps/gems
    solution_map = {}
    for var in solution:
        solution_map[abs(var)] = (var > 0)  # True = trap, False = gem

    # Translate solution to the grid for visualization
    grid_solution = [[grid[r][c] if isinstance(grid[r][c], int) else None for c in range(len(grid[0]))] for r in range(len(grid))]
    for (row, col), logical_var in logical_vars.items():
        if grid_solution[row][col] is None:
            grid_solution[row][col] = "T" if solution_map.get(logical_var, False) else "G"

    # Print the interpreted grid solution
    print("Grid Solution:")
    for row in grid_solution:
        print(row)
else:
    print("No solution could be found.")

# Clean up the solver resources
solver.delete()
