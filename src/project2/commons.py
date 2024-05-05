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

def print_sat(value, board, row, col, flag = 0):
    if flag == 0:
        for var in value:
            if board[(abs(var) - 1) // col][(abs(var) - 1) % col] == -1:
                board[(abs(var) - 1) // col][(abs(var) - 1) % col] = (
                    "T" if var > 0 else "G"
                )
        for sublist in board:
            print(", ".join(map(str, sublist)))
    elif flag == 1:
        for index, val in enumerate(value):
            if board[index // col][index % col] == -1:
                board[index // col][index % col] = (
                    "G" if val == 0 else "T"
                )
        for sublist in board:
            print(", ".join(map(str, sublist)))