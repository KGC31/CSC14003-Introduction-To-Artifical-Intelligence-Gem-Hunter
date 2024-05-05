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

def solve_sat_backtracking(cnf):
    num_vars = max([abs(literal) for clause in cnf for literal in clause])
    assignment = [None] * num_vars
    if backtrack(cnf, assignment, 0):
        return assignment
    else:
        return None

def backtrack(cnf, assignment, var_index):
    if var_index == len(assignment):
        return is_satisfying_assignment(assignment, cnf)

    assignment[var_index] = True
    if backtrack(cnf, assignment, var_index + 1):
        return True

    assignment[var_index] = False
    if backtrack(cnf, assignment, var_index + 1):
        return True

    assignment[var_index] = None
    return False

def solve():
    filename = "input.txt"  
    board = read_input(filename)
    row = len(board)
    col = len(board[0])

    cnf = read_cnf_file("clauses.cnf")
    solution = solve_sat_backtracking(cnf)

    if solution:
        print("SAT")
        solution = [int(val) for val in solution]
        print(solution)
        print_sat(solution, board, row, col, flag=1)

    else:
        print("UNSAT")

solve()
