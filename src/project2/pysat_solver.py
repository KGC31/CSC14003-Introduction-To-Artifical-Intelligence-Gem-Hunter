from pysat import solvers
from commons import read_input, print_sat

def solve_sat(cnf_file_path, board, row, col):
    # Create a solver instance
    solver = solvers.Glucose3()
    ans_board = board
    # Load the CNF file
    with open(cnf_file_path, 'r') as f:
        cnf = f.read()

    # Parse and add the CNF formula to the solver
    clauses = [[int(literal) for literal in line.split() if literal != '0'] for line in cnf.splitlines() if line and line[0] not in ('c', 'p')]
    for clause in clauses:
        solver.add_clause(clause)

    # Solve the SAT problem
    if solver.solve():
        # Check the value of a boolean variable (e.g., variable 1)
        variable_value = solver.get_model()
        print_sat(variable_value, ans_board, row, col)
    else:
        # If UNSAT, print UNSAT
        print("UNSAT")

def solve():
    filename = "input.txt"  
    board = read_input(filename)
    row = len(board)
    col = len(board[0])

    solve_sat("clauses.cnf", board, row, col)

solve()
