from commons import read_input, print_sat

def read_cnf_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    cnf = []
    for line in lines:
        if line.startswith('c') or line.startswith('p'):
            continue
        clause = [int(literal) for literal in line.split() if literal != '0']
        cnf.append(clause)
    return cnf

def brute_force_sat(cnf):
    num_vars = max([abs(literal) for clause in cnf for literal in clause])
    for i in range(2 ** num_vars):
        assignment = [bool((i >> j) & 1) for j in range(num_vars)]
        if is_satisfying_assignment(assignment, cnf):
            return assignment
    return None

def is_satisfying_assignment(assignment, cnf):
    for clause in cnf:
        clause_satisfied = False
        for literal in clause:
            var = abs(literal) - 1
            if (literal > 0 and assignment[var]) or (literal < 0 and not assignment[var]):
                clause_satisfied = True
                break
        if not clause_satisfied:
            return False
    return True

def solve():
    filename = "input.txt"  
    board = read_input(filename)
    row = len(board)
    col = len(board[0])

    cnf = read_cnf_file("clauses.cnf")
    solution = brute_force_sat(cnf)

    if solution:
        print("SAT")
        solution = [int(val) for val in solution]
        print(solution)
        print_sat(solution, board, row, col, flag=1)

    else:
        print("UNSAT")

solve()