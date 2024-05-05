import copy
from utils import *
import time

adjacents = [[0, 1], [1, 0], [1, 1], [-1, 0], [0, -1], [-1, -1], [-1, 1], [1, -1]]
result = []

def is_valid(grid, cell):
    for direction in adjacents:
        pos = [cell[0] + direction[0], cell[1] + direction[1]]
        if 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0]) and isinstance(grid[pos[0]][pos[1]], int):
            if grid[pos[0]][pos[1]] <= 0:
                return False 
    return True

def update_map(grid, cell):
    for direction in adjacents:
        pos = [cell[0] + direction[0], cell[1] + direction[1]]
        if 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0]) and isinstance(grid[pos[0]][pos[1]], int):
            grid[pos[0]][pos[1]] -= 1


def backtrack(grid, y, x):
    # Stop condition
    if y == len(grid):
        for j in range(len(grid)):
            for i in range(len(grid[0])):
                if grid[j][i] == 1:
                    return False
        global result
        for i in range (len(grid)):
            for j in range (len(grid[0])):
                if not isinstance(grid[i][j], int):
                    result[i][j] = grid[i][j]
        return True
    
    # Update next position
    next_y = y if x + 1 < len(grid[0]) else y + 1
    next_x = (x + 1) % len(grid[0])

    # Begin backtracking
    if grid[y][x] == "_":
        if is_valid(grid, [y, x]):
            # Let the current cell be "T"
            temp = copy.deepcopy(grid)  # Create a deep copy of the grid
            update_map(temp, [y, x])
            temp[y][x] = "T"
            if backtrack(temp, next_y, next_x):
                return True
            
            # Revert the cell back to "_"
            grid[y][x] = "_"
            
            # Try "G" otherwise
            grid[y][x] = "G"
            if backtrack(grid, next_y, next_x):
                return True
        else:
            # If assigning "T" is not valid, assign "G"
            grid[y][x] = "G"
            if backtrack(grid, next_y, next_x):
                return True
            return False
    
    return backtrack(grid, next_y, next_x)


# Driver Code
if __name__ == "__main__":
    file_name = input('Input grid name: ')
    grid = read_grid('maps/' + file_name)

    result = copy.deepcopy(grid)
    if grid:
        start = time.time()
        if backtrack(grid, 0, 0):
            print_grid(result)
        else:
            print("No solution exists.")
        end = time.time()
        print("Runtime:", end - start, "seconds")
    else:
        print("No grid loaded.")
