import copy
from pysat.formula import CNF

from pysat.solvers import Solver


def read_input(filename):
    pattern = []
    with open(filename, "r") as file:
        for line in file:
            row = line.strip().split(",")
            row = [-1 if x == " _" else x for x in row]
            row = [-1 if x == "_" else x for x in row]

            pattern.append(row)
    pattern = [[int(x) for x in row] for row in pattern]

    return pattern


def find_all_clauses(
    input_array, input_len, combi_len, indi_tup, ans_index, next_start, clause_tup
):
    for iter in range(next_start, input_len + 1):
        if combi_len <= 0:
            clause_tup.append(copy.copy(indi_tup))
            return
        indi_tup[ans_index] = input_array[iter]
        find_all_clauses(
            input_array,
            input_len,
            combi_len - 1,
            indi_tup,
            ans_index + 1,
            iter + 1,
            clause_tup,
        )


def find_cell_no(i, j, row, col):
    return i * col + j + 1


def find_adjacent_cells(board, i, j, row, col):
    output = []
    if i >= 1 and j >= 1:
        output.append(find_cell_no(i - 1, j - 1, row, col))
    if i >= 1:
        output.append(find_cell_no(i - 1, j, row, col))
    if i >= 1 and j < (col - 1):
        output.append(find_cell_no(i - 1, j + 1, row, col))
    if j < (col - 1):
        output.append(find_cell_no(i, j + 1, row, col))
    if i < (row - 1) and j < (col - 1):
        output.append(find_cell_no(i + 1, j + 1, row, col))
    if i < (row - 1):
        output.append(find_cell_no(i + 1, j, row, col))
    if i < (row - 1) and j >= 1:
        output.append(find_cell_no(i + 1, j - 1, row, col))
    if j >= 1:
        output.append(find_cell_no(i, j - 1, row, col))
    for cell in output:
        if board[(cell - 1) // col][(cell -1) % col] != -1:
            output.remove(cell)
    return output

def generate_cnf(board, row, col):
    cnf = CNF()
    for i in range(row):
        for j in range(col):
            if board[i][j] != -1:
                adj_cells = find_adjacent_cells(board, i, j, row, col)
                count_adj = len(adj_cells)
                adj_cells.append(0)  # Why appending 0 here? Seems incorrect and might need removal.
                indi_tup = [0] * (board[i][j] + 1)
                first_tup = []
                find_all_clauses(adj_cells, count_adj, board[i][j] + 1, indi_tup, 0, 0, first_tup)
                for tups in first_tup:
                    cnf.append([-x for x in tups])  # Negative clauses
                indi_tup = [0] * (count_adj - board[i][j] + 1)
                second_tup = []
                find_all_clauses(adj_cells, count_adj, count_adj - board[i][j] + 1, indi_tup, 0, 0, second_tup)
                for tups in second_tup:
                    cnf.append(tups)  # Positive clauses
    return cnf

def execution(board, row, col):
    cnf = generate_cnf(board, row, col)
    s = Solver()
    s.append_formula(cnf.clauses)
    is_sat = s.solve()

    if is_sat:
        variable_value = s.get_model()
        for var in variable_value:
            if var > 0:
                i, j = divmod(var - 1, col)
                if board[i][j] == -1:
                    board[i][j] = 'T'
            else:
                i, j = divmod(-var - 1, col)
                if board[i][j] == -1:
                    board[i][j] = 'G'
        for sublist in board:
            print(', '.join(map(str, sublist)))
    else:
        print("No solution found")

filename = "input.txt"  # Change this to your file path
board = read_input(filename)
row = len(board)
col = len(board[0])
execution(board, row, col)

def dpll(clauses, assignment):
    if not clauses:
        return True, assignment
    if any(not clause for clause in clauses):
        return False, None

    # Unit propagation
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses.pop()
        var = unit[0]
        if -var in assignment:
            return False, None
        assignment.add(var)
        # Update clauses
        clauses = [c for c in clauses if var not in c]
        clauses = [[x for x in c if x != -var] for c in clauses]
        unit_clauses = [c for c in clauses if len(c) == 1]

    # Choose variable to assign
    for clause in clauses:
        for var in clause:
            if var not in assignment and -var not in assignment:
                break
        else:
            continue
        break
    else:
        return False, None  # No variable found, should not happen

    # Try true assignment
    solvable, new_assignment = dpll(clauses, assignment | {var})
    if solvable:
        return True, new_assignment

    # Try false assignment
    return dpll(clauses, assignment | {-var})

def solve_cnf(board, row, col):
    clauses = generate_cnf(board, row, col)  # Assume function to generate CNF from board
    solvable, assignment = dpll(clauses, set())
    if solvable:
        for var in assignment:
            if var > 0:
                i, j = divmod(var - 1, col)
                board[i][j] = 'T'
            elif var < 0:
                i, j = divmod(-var - 1, col)
                board[i][j] = 'G'
        print_board(board)
    else:
        print("No solution found")

# Định nghĩa hàm print_board nếu cần
def print_board(board):
    for row in board:
        print(' '.join(str(cell) for cell in row))
