import os
from typing import List, Tuple
from dataclasses import dataclass

from utils.timer import timer
from utils.utils import tcolors

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


@dataclass
class Coordinate:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


@timer
def part1():
    # TODO: Implement part 1
    instructions = parse_file("input_sample01.txt")
    print(f"Instructions: {instructions}")

    pos = Coordinate(0, 0)
    dir = Coordinate(-1, 0)
    boundaries = (Coordinate(0, 0), Coordinate(0, 0))
    corners = [pos]

    for instruction in instructions:
        # print(f"{tcolors.BLUE}Instruction: {instruction}{tcolors.RESET}")
        # print(f"{tcolors.RED}Current position: {pos}{tcolors.RESET}")
        # print(f"{tcolors.RED}Current direction: {dir}{tcolors.RESET}")

        side, length = instruction[0], int(instruction[1:])

        if side == "R":
            pos = Coordinate(pos.x + dir.y * length, pos.y - dir.x * length)
            dir.x, dir.y = dir.y, -dir.x
        else:
            pos = Coordinate(pos.x - dir.y * length, pos.y + dir.x * length)
            dir.x, dir.y = -dir.y, dir.x

        # print(f"{tcolors.GREEN}New position: {pos}{tcolors.RESET}")
        # print(f"{tcolors.GREEN}New direction: {dir}{tcolors.RESET}")
        corners.append(pos)
        boundaries = (
            Coordinate(min(boundaries[0].x, pos.x), min(boundaries[0].y, pos.y)),
            Coordinate(max(boundaries[1].x, pos.x), max(boundaries[1].y, pos.y)),
        )

    print(f"Boundaries: {boundaries}")
    tunnel = build_tunnel(corners, boundaries)
    print_tunnel(tunnel)


# (-1, 0) (0, 0) -> R3 -> (-3, 0) (0 +   0 , 0 - (-3)) (0, 3)
# ( 0, 1) (0, 3) -> R4 -> ( 0, 4) (0 +   4 , 3 +   0 ) (4, 3)
# ( 1, 0) (4, 3) -> L3 -> ( 3, 0) (4 +   0 , 3 +   3 ) (4, 6)
# ( 0, 1) (4, 6) -> L4 -> ( 0, 4) (4 -   4 , 6 +   0 ) (0, 6)
# (-1, 0) (0, 6) -> R3 -> (-3, 0) (0 +   0 , 6 - (-3)) (0, 9)
# ( 0, 1) (0, 9) -> R6 -> ( 0, 6) (0 +   6 , 9 +   0 ) (6, 9)
# ( 1, 0) (6, 9) -> R9 -> ( 9, 0) (6 +   0 , 9 -   9 ) (6, 0)


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


def build_tunnel(
    corners: List[Coordinate], boundaries: Tuple[Coordinate]
) -> List[List[str]]:
    shift_x = abs(boundaries[0].x) if boundaries[0].x < 0 else 0
    shift_y = abs(boundaries[0].y) if boundaries[0].y < 0 else 0

    # Add 1 to include the starting point
    size_x = abs(boundaries[0].x) + abs(boundaries[1].x) + 1
    size_y = abs(boundaries[0].y) + abs(boundaries[1].y) + 1

    tunnel = [[" " for _ in range(size_y)] for _ in range(size_x)]

    # Fill the walls
    pos = corners[0]
    for corner in corners[1:]:
        dir = get_direction(pos, corner)
        if pos.x == corner.x:
            for i in range(pos.y + shift_y, corner.y + dir.y + shift_y, dir.y):
                tunnel[pos.x + shift_x][i] = "#"
        else:
            for i in range(pos.x + shift_x, corner.x + dir.x + shift_x, dir.x):
                tunnel[i][pos.y + shift_y] = "#"

        pos = corner
    
    # TODO I think this sucks
    tunnel.insert(0, ["#"] * size_y)
    tunnel.append(["#"] * size_y)
    for i in range(size_x+2):
        tunnel[i].insert(0, "#")
        tunnel[i].append("#")

    return tunnel


def print_tunnel(tunnel: List[List[str]]) -> None:
    for row in tunnel:
        print("".join(row))


def get_direction(pos1: Coordinate, pos2: Coordinate) -> Coordinate:
    return Coordinate(
        (pos2.x - pos1.x) // abs(pos2.x - pos1.x) if pos2.x != pos1.x else 0,
        (pos2.y - pos1.y) // abs(pos2.y - pos1.y) if pos2.y != pos1.y else 0,
    )


def parse_file(file_name: str) -> Tuple[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    instructions = []
    with open(abs_file_path, "r") as f:
        instructions = f.read().strip().split(",")
    return instructions


part1()
# part2()
# part3()
