import copy

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
        if board[(cell - 1) // col][(cell - 1) % col] != -1:
            output.remove(cell)
    return output


def gen_cnf(board, row, col):
    fout = open("clauses.cnf", "w")
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

                for k in range(len(first_tup)):
                    for l in range(board[i][j] + 1):
                        fout.write(str(-1 * first_tup[k][l]) + " ")
                    fout.write("0\n")

                indi_tup = []
                for k in range(count_adj - board[i][j] + 1):
                    indi_tup.append(0)
                second_tup = []
                find_all_clauses(
                    adj_cells,
                    count_adj,
                    count_adj - board[i][j] + 1,
                    indi_tup,
                    0,
                    0,
                    second_tup,
                )
                for k in range(len(second_tup)):
                    for l in range(count_adj - board[i][j] + 1):
                        fout.write(str(second_tup[k][l]) + " ")
                    fout.write("0\n")

filename = "input.txt"  # Change this to your file path
board = read_input(filename)
row = len(board)
col = len(board[0])
gen_cnf(board, row, col)
