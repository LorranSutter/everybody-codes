import os
import re
import math
from dataclasses import dataclass
from typing import List, Tuple

from utils.timer import timer

"""
Preprocessing:
- Created a dataclass Snail with attributes x, y, and path.
    - The "path" is the size of the path the snail can travel, that is calculated by (x + y - 1)
- We read the input file and return a list of Snail objects.

Part 1:
- We just want the final position of the snail after N days, so we do the following:
    - We take de modulus of the number of days by the size of snails' path, so we get how far the snail will be from its initial position (offset).
    - Then we have to calculate x and y:
        - For x, we add offset to the initial x position. If the result is greater than the path, we just get the modulus of the result.
        - For y, since the path is calculated by (path = x + y - 1), we can just do (new_y = path + 1 - new_x)
- In each iteration, we calculate the result by the given formula and sum all them up to get the final result.

Part 2:
- Things get interesting here.
- We know that every snail must reach y = 1 at the same time, so we can get the amount of days to reach it by 
    - offset = y - 1
- If we consider each snail individually, we can easily assume the total days will be
    - total_days = offset
- If we start with the first snail, the total days will be the offset of this snail.
- For the second snail, we can only increment days passed by the preovious snail until both reaches y = 1
- After the second snail reaches y = 1, we can calculate the total_path that the following snail will walk
    - total_path = LCM(snail_path, current_total_path) - least common multiple between the current snails' size path and the current total path
- We continue iterating over all remaining snails.
- Finally, we return the the total days passed.

Part 3:
- Same as part 1, but with larger numbers.

Obs: Part 2 could be solved by brute force, iterating over all snails until every snail reaches y = 1.
"""


@dataclass
class Snail:
    x: int
    y: int
    path: int


@timer
def part1():
    snails = parse_file("input01.txt")
    days = 100

    print("Initial grid:")
    print_grid(snails)

    sum_pos = 0
    for snail in snails:
        offset = days % snail.path

        snail.x += offset
        if snail.x > snail.path:
            snail.x %= snail.path

        # Update y based on the new x
        snail.y = snail.path + 1 - snail.x

        sum_pos += snail.x + (days * snail.y)

    print(f"Grid after {days} days:")
    print_grid(snails)

    print(f"Sum of all snails' positions after {days} days: {sum_pos}")


@timer
def part2():
    snails = parse_file("input02.txt")
    print("Grid before golden line:")
    print_grid(snails)

    total_days = calculate_days_to_golden_line(snails)

    print(f"Total days to align on the golden line: {total_days}")


@timer
def part3():
    snails = parse_file("input03.txt")
    print("Grid before golden line:")
    print_grid(snails)

    total_days = calculate_days_to_golden_line(snails)

    print(f"Total days to align on the golden line: {total_days}")


def calculate_days_to_golden_line(snails: List[Snail]) -> int:
    total_days = 0
    total_path = 1
    for snail in snails:

        offset = snail.y - 1

        while (total_days - offset) % snail.path != 0:
            total_days += total_path

        total_path = math.lcm(snail.path, total_path)

    return total_days


def print_grid(snails: List[Snail]):
    max_path = 0
    for snail in snails:
        if snail.path > max_path:
            max_path = snail.path

    grid = [["."] * (max_path + 1) for _ in range(max_path + 1)]

    for snail in snails:
        x, y = snail.x, snail.y
        grid[y - 1][x - 1] = "#"

    x = max_path
    for i in range(max_path + 1):
        for j in range(x):
            print(grid[i][j], end=" ")
        print()
        x -= 1


def parse_file(file_name: str) -> List[Tuple[int, int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    snails = []
    with open(abs_file_path, "r") as f:
        for line in f:
            pos = re.match(r"x=(\d+)\s+y=(\d+)", line).groups()
            pos = tuple(map(int, pos))
            snails.append(Snail(*pos, pos[0] + pos[1] - 1))
    return snails


part1()
part2()
part3()
