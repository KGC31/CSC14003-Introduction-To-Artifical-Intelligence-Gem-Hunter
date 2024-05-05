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


def execution(board, row, col):
    cnf = CNF()

    ans_board = board
    for i in range(row):
        for j in range(col):
            if board[i][j] != -1:
                adj_cells = find_adjacent_cells(board, i, j, row, col)
                count_adj = len(adj_cells)
                adj_cells.append(0)
                indi_tup = []
                for k in range(board[i][j] + 1):
                    indi_tup.append(0)
                # print indi_tup
                first_tup = []
                find_all_clauses(
                    adj_cells, count_adj, board[i][j] + 1, indi_tup, 0, 0, first_tup
                )
                for tups in first_tup:
                    cnf.append([-x for x in tups])
                indi_tup = []
                for k in range(count_adj - board[i][j] +1):
                    indi_tup.append(0)
                second_tup =[]
                find_all_clauses(adj_cells,count_adj,count_adj-board[i][j]+1,indi_tup,0,0,second_tup)
                for tups in second_tup:
                    cnf.append(tups)

    s = Solver()
    s.append_formula(cnf.clauses)
    # Solve the CNF
    is_sat = s.solve()

    # Check the value of a boolean variable (e.g., variable 1)
    variable_value = s.get_model()

    for var in variable_value:
        if board[(abs(var) - 1) // col][(abs(var) -1) % col] == -1:
            ans_board[(abs(var) - 1) // col][(abs(var) -1) % col] = 'T' if var >0 else 'G' 


    for sublist in ans_board:
        print(', '.join(map(str, sublist)))

                


filename = "input.txt"  # Change this to your file path
board = read_input(filename)
row = len(board)
col = len(board[0])
execution(board, row, col)
