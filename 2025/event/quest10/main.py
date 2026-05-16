import os
from typing import List, Tuple

from utils.timer import timer
from utils.utils import print_matrix

"""
Preprocessing:
-

Part 1:
-

Part 2:
-

Part 3:
-
"""


@timer
def part1():
    grid, grid_size, dragon = parse_file("input_sample01.txt")

    move_grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    calculate_move_grid(move_grid, grid_size, dragon, 3)
    print_matrix(move_grid)

    in_range = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if move_grid[i][j] == "X" and grid[i][j] == "S":
                in_range += 1
    
    print(f"Sheep in range of the dragon move: {in_range}")


@timer
def part2():
    # TODO: Implement part 2
    lines = parse_file("input_sample02.txt")
    pass


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file("input_sample03.txt")
    pass

def calculate_move_grid(grid: List[List[str]], grid_size: int, dragon: Tuple[int, int], moves: int) -> List[List[str]]:
    if moves < 0:
        return grid
    if dragon[0] < 0 or dragon[0] >= grid_size or dragon[1] < 0 or dragon[1] >= grid_size:
        return grid

    grid[dragon[0]][dragon[1]] = "X"
    grid[grid_size - 1 - dragon[0]][grid_size - 1 - dragon[1]] = "X"
    
    calculate_move_grid(grid, grid_size, (dragon[0] + 2, dragon[1] + 1), moves - 1)
    calculate_move_grid(grid, grid_size, (dragon[0] + 2, dragon[1] - 1), moves - 1)
    # calculate_move_grid(grid, grid_size, (dragon[0] - 2, dragon[1] + 1), moves - 1)
    # calculate_move_grid(grid, grid_size, (dragon[0] - 2, dragon[1] - 1), moves - 1)
    calculate_move_grid(grid, grid_size, (dragon[0] + 1, dragon[1] + 2), moves - 1)
    calculate_move_grid(grid, grid_size, (dragon[0] + 1, dragon[1] - 2), moves - 1)
    # calculate_move_grid(grid, grid_size, (dragon[0] - 1, dragon[1] + 2), moves - 1)
    # calculate_move_grid(grid, grid_size, (dragon[0] - 1, dragon[1] - 2), moves - 1)


def parse_file(file_name: str) -> Tuple[List[str], int, Tuple[int, int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    grid = []
    dragon = None
    grid_size = 0
    with open(abs_file_path, "r") as f:
        for line in f:
            line = [elem for elem in line.strip()]
            grid.append(line)

            if not dragon and "D" in line:
                dragon = (len(grid) - 1, line.index("D"))

        grid_size = len(grid)

    return grid, grid_size, dragon


part1()
# part2()
# part3()
