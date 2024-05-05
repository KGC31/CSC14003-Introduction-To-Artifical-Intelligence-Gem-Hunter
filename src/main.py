import copy
import time
from pysat.formula import CNF
from pysat.solvers import Solver

def read_input(filename):
    pattern = []
    with open(filename, "r") as file:
        for line in file:
            row = line.strip().split()
            row = [-1 if x == "_" else int(x) for x in row]
            pattern.append(row)
    return pattern

def find_all_clauses(input_array, combi_len):
    clause_tup = []
    input_len = len(input_array)
    for iter in range(input_len - combi_len + 1):
        indi_tup = input_array[iter:iter + combi_len]
        clause_tup.append(indi_tup)
    return clause_tup

def find_cell_no(i, j, col):
    return i * col + j + 1

def find_adjacent_cells(board, i, j, row, col):
    output = []
    for x in range(max(0, i - 1), min(i + 2, row)):
        for y in range(max(0, j - 1), min(j + 2, col)):
            if (x, y) != (i, j) and board[x][y] == -1:
                output.append(find_cell_no(x, y, col))
    return output

def pysat_solver(board, row, col):
    cnf = CNF()

    for i in range(row):
        for j in range(col):
            if board[i][j] != -1:
                adj_cells = find_adjacent_cells(board, i, j, row, col)
                count_adj = len(adj_cells)
                first_tup = find_all_clauses(adj_cells, board[i][j] + 1)
                for tups in first_tup:
                    cnf.append([-x for x in tups])
                second_tup = find_all_clauses(adj_cells, count_adj - board[i][j] + 1)
                cnf.extend(second_tup)

    s = Solver()
    s.append_formula(cnf.clauses)
    is_sat = s.solve()

    if is_sat:
        variable_value = s.get_model()
        for var in variable_value:
            i = (abs(var) - 1) // col
            j = (abs(var) - 1) % col
            if board[i][j] == -1:
                board[i][j] = 'T' if var > 0 else 'G'
        for sublist in board:
            print(' '.join(map(str, sublist)))
    else:
        print("No solution found")

# Driver code
if __name__ == '__main__':
    file_name = input('Input grid name: ')

    board = read_input('maps/' + file_name)
    row = len(board)
    col = len(board[0])

    start = time.time()
    # Execute pysat CNF solver
    pysat_solver(board, row, col)
    end = time.time()
    print("Runtime:", end - start, "seconds")