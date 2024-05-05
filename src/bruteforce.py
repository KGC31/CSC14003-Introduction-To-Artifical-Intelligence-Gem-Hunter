from itertools import product
from utils import read_grid
import time

adjacents = [[0, 1], [1, 0], [1, 1], [-1, 0], [0, -1], [-1, -1], [-1, 1], [1, -1]]

def is_valid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if isinstance(grid[i][j], int):
                count = 0
                for direction in adjacents:
                    x, y = i + direction[0], j + direction[1]
                    if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == "T":
                        count += 1
                if count != grid[i][j]:
                    return False
    return True

def brute_force(grid):
    possibilities = []

    # Iterate through each cell in the grid
    for row in grid:
        for cell in row:
            # If the cell is empty, add "T" and "_" to the possibilities list
            if cell == "_":
                possibilities.append(["T", "_"])
            # If the cell contains a number, add it to the possibilities list
            elif isinstance(cell, int):
                possibilities.append([cell])

    # Generate all combinations of possibilities
    all_possibilities = list(product(*possibilities))
    for possibility in all_possibilities:
        curr = []
        for i in range(len(grid)):
            temp = []
            for j in range(len(grid[0])):
                temp.append(possibility[i*4 + j])
            curr.append(temp)
        if is_valid(curr):
            for i in range(len(curr)):
                for j in range(len(curr[0])):
                    if curr[i][j] == "_":
                        curr[i][j] = "G"  # Change empty cells to "G"
            return curr
    return None

if __name__ == "__main__":
    file_name = input('Input grid name: ')
    grid = read_grid('maps/' + file_name)
    
    if grid:
        start = time.time()
        solution = brute_force(grid)
        if solution:
            for row in solution:
                print(' '.join(map(str, row)))
        else:
            print("No solution exists.")
        end = time.time()
        print("Runtime:", end - start, "seconds")
    else:
        print("No grid loaded.")
