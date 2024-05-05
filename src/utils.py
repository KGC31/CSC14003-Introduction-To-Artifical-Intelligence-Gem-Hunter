def read_grid(filename):
    try:
        with open(filename, 'r') as file:
            grid = [[int(cell) if cell.isdigit() else cell for cell in line.strip().split()] for line in file.readlines()]
        return grid
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
