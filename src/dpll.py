from itertools import combinations
from utils import read_grid

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
            for combo in combinations(neighbor_vars, clue_number):
                clause = []
                for var in neighbor_vars:
                    if var in combo:
                        clause.append(var)
                    else:
                        clause.append(-var)
                cnf_clauses.append(clause)

# DPLL Algorithm
def dpll(clauses, assignment={}):
    # Simplify clauses and apply unit propagation
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses.pop()
        literal = unit[0]
        assignment[abs(literal)] = literal > 0
        clauses = [clause for clause in clauses if literal not in clause]
        for i in range(len(clauses)):
            clause = clauses[i]
            if -literal in clause:
                clause = [x for x in clause if x != -literal]
                if not clause:
                    return False, None  # Conflict found
                clauses[i] = clause
        unit_clauses = [c for c in clauses if len(c) == 1]

    # Check if all clauses are satisfied
    if not clauses:
        return True, assignment

    # Select the first unassigned variable
    for var in range(1, var_counter):
        if var not in assignment:
            break

    # Recur with var set to True
    sat, result = dpll(clauses + [[var]], assignment.copy())
    if sat:
        return sat, result

    # Recur with var set to False
    sat, result = dpll(clauses + [[-var]], assignment.copy())
    if sat:
        return sat, result

    return False, None

# Driver code
if __name__ == '__main__':
    file_name = input('Input grid name: ')
    grid = read_grid('maps/' + file_name)
    
    sat, assignment = dpll(cnf_clauses)
    if sat:
        print("Solution found:", assignment)
        # Translate the assignment back to the grid representation
        solution_grid = []
        for r in range(len(grid)):
            row_solution = []
            for c in range(len(grid[0])):
                if grid[r][c] != '_':
                    row_solution.append(grid[r][c])
                else:
                    var = logical_vars[(r, c)]
                    row_solution.append('T' if assignment.get(var, False) else 'G')
            solution_grid.append(row_solution)
        print("Grid solution:")
        for row in solution_grid:
            print(row)
    else:
        print("No solution could be found.")
