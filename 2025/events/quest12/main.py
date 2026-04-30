import os
import sys
from typing import List, Set, Tuple

from utils.timer import timer
from utils.utils import tcolors

sys.setrecursionlimit(2000)

"""
Preprocessing:
- Read the input file and parse the grid into a 2D array of integers.
- We can add a border of -1 around the grid to avoid out-of-bounds checks during DFS.

Part 1:
- Apply simple DFS from the starting point (1, 1) to mark the barrels that are ignited.

Part 2:
- There is an advantage here: the result chain reaction for each barrel is independent.
- We can just run the same DFS for each barrel and keep track of the maximum number of ignited barrels individually.

Part 3:
- This is a little bit brute force approach.
- First, we run DFS for each barrel to find the one that ignites the most barrels.
- Then we mark those barrels as ignited, and replace their values with -1 in the grid to prevent them from igniting others in the next rounds.
- We repeat the process as much rounds as we want, and keep track of the total ignited barrels.

Obs: There is a nice draw in each part after igniting the barrels
    - Part 1 shows a big X
    - Part 2 shows a spiraling pattern
    - Part 3 has an easter egg: shows a duck!
"""


@timer
def part1():
    grid = parse_file("input01.txt")

    visited = set()
    ignited = set()
    dfs(grid, (1, 1), visited, ignited)

    print_grid(grid, ignited)
    print(f"Total ignited barrels: {len(ignited)}")


@timer
def part2():
    grid = parse_file("input02.txt")

    visited = set()
    ignited = set()
    dfs(grid, (1, 1), visited, ignited)
    dfs(grid, (len(grid) - 2, len(grid[0]) - 2), visited, ignited)

    print_grid(grid, ignited)
    print(f"Total ignited barrels: {len(ignited)}")


@timer
def part3():
    grid_original = parse_file("input_sample03.txt")
    grid = [row[:] for row in grid_original]

    already_ignited = set()
    for _ in range(3):

        initial_barrel = (1,1)
        most_ignited_count = 0
        most_ignited_list = []

        for i in range(1, len(grid) - 1):
            for j in range(1, len(grid[0]) - 1):
                if (i, j) in already_ignited:
                    continue

                visited = set()
                ignited = set()
                dfs(grid, (i, j), visited, ignited)

                if len(ignited) > most_ignited_count:
                    initial_barrel = (i, j)
                    most_ignited_count = len(ignited)
                    most_ignited_list = ignited
        
        already_ignited.update(most_ignited_list)

        for ignited_barrel in most_ignited_list:
            grid[ignited_barrel[0]][ignited_barrel[1]] = -1

        print(f"\nRound {_ + 1}:")
        print(f"Initial barrel: {initial_barrel}, Grid value: {grid[initial_barrel[0]][initial_barrel[1]]}")
        print(f"Most ignited count: {most_ignited_count}" )
        print_grid(grid_original, most_ignited_list)


    print("\nFinal grid:")
    print_grid(grid_original, already_ignited)

    print(f"Total ignited barrels: {len(already_ignited)}")


def dfs(grid: List[List[int]], barrel: Tuple[int], visited: Set, ignited: Set) -> None:
    visited.add(barrel)
    if grid[barrel[0]][barrel[1]] == -1:
        return

    ignited.add((barrel[0], barrel[1]))
    barrel_size = grid[barrel[0]][barrel[1]]

    if (
        grid[barrel[0] + 1][barrel[1]] <= barrel_size
        and (barrel[0] + 1, barrel[1]) not in visited
    ):
        dfs(grid, (barrel[0] + 1, barrel[1]), visited, ignited)
    if (
        grid[barrel[0] - 1][barrel[1]] <= barrel_size
        and (barrel[0] - 1, barrel[1]) not in visited
    ):
        dfs(grid, (barrel[0] - 1, barrel[1]), visited, ignited)
    if (
        grid[barrel[0]][barrel[1] + 1] <= barrel_size
        and (barrel[0], barrel[1] + 1) not in visited
    ):
        dfs(grid, (barrel[0], barrel[1] + 1), visited, ignited)
    if (
        grid[barrel[0]][barrel[1] - 1] <= barrel_size
        and (barrel[0], barrel[1] - 1) not in visited
    ):
        dfs(grid, (barrel[0], barrel[1] - 1), visited, ignited)


def print_grid(grid: List[List[int]], ignited: List[Tuple[int]]) -> None:
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            if (i, j) in ignited:
                print(f"{tcolors.RED}{grid[i][j]}{tcolors.RESET}", end="")
            else:
                print(grid[i][j], end="")
        print()


def parse_file(file_name: str) -> List[List[int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    grid = []
    with open(abs_file_path, "r") as f:
        for line in f:
            grid.append([-1] + [int(x) for x in line.strip()] + [-1])

    grid.insert(0, [-1] * (len(grid[0])))
    grid.append([-1] * (len(grid[0]) + 2))
    return grid


part1()
part2()
part3()
