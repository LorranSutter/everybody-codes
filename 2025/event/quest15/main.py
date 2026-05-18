import os
from typing import List, Tuple
from collections import deque
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


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


@timer
def part1():
    instructions = parse_file("input01.txt")
    print(f"Instructions: {instructions}")

    corners, boundaries = find_corners_and_boundaries(instructions, (0, 0))
    tunnel, corners = build_tunnel(corners, boundaries)
    path_length, path = find_shortest_path_with_trace(tunnel, corners[0], corners[-1])

    for cell in path:
        tunnel[cell.x][cell.y] = tcolors.GREEN + "." + tcolors.RESET

    print_tunnel(tunnel)

    print(f"Shortest path length: {path_length-1}")


# (-1, 0) (0, 0) -> R3 -> (-3, 0) (0 +   0 , 0 - (-3)) (0, 3)
# ( 0, 1) (0, 3) -> R4 -> ( 0, 4) (0 +   4 , 3 +   0 ) (4, 3)
# ( 1, 0) (4, 3) -> L3 -> ( 3, 0) (4 +   0 , 3 +   3 ) (4, 6)
# ( 0, 1) (4, 6) -> L4 -> ( 0, 4) (4 -   4 , 6 +   0 ) (0, 6)
# (-1, 0) (0, 6) -> R3 -> (-3, 0) (0 +   0 , 6 - (-3)) (0, 9)
# ( 0, 1) (0, 9) -> R6 -> ( 0, 6) (0 +   6 , 9 +   0 ) (6, 9)
# ( 1, 0) (6, 9) -> R9 -> ( 9, 0) (6 +   0 , 9 -   9 ) (6, 0)


@timer
def part2():
    instructions = parse_file("input02.txt")
    print(f"Instructions: {instructions}")

    corners, boundaries = find_corners_and_boundaries(instructions, (0, 0))
    tunnel, corners = build_tunnel(corners, boundaries)
    path_length, path = find_shortest_path_with_trace(tunnel, corners[0], corners[-1])

    for cell in path:
        tunnel[cell.x][cell.y] = tcolors.GREEN + "." + tcolors.RESET

    print_tunnel(tunnel)

    print(f"Shortest path length: {path_length-1}")


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file("input_sample03.txt")
    pass


def find_corners_and_boundaries(
    instructions: List[str], start: Tuple[int, int]
) -> Tuple[List[Coordinate], Tuple[Coordinate, Coordinate]]:
    pos = Coordinate(start[0], start[1])
    dir = Coordinate(-1, 0)
    boundaries = (Coordinate(0, 0), Coordinate(0, 0))
    corners = [pos]
    for instruction in instructions:
        side, length = instruction[0], int(instruction[1:])

        if side == "R":
            pos = Coordinate(pos.x + dir.y * length, pos.y - dir.x * length)
            dir = Coordinate(dir.y, -dir.x)
        else:
            pos = Coordinate(pos.x - dir.y * length, pos.y + dir.x * length)
            dir = Coordinate(-dir.y, dir.x)

        corners.append(pos)
        boundaries = (
            Coordinate(min(boundaries[0].x, pos.x), min(boundaries[0].y, pos.y)),
            Coordinate(max(boundaries[1].x, pos.x), max(boundaries[1].y, pos.y)),
        )

    return corners, boundaries


def build_tunnel(
    corners: List[Coordinate], boundaries: Tuple[Coordinate]
) -> Tuple[List[List[str]], List[Coordinate]]:
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
    for i in range(size_x + 2):
        tunnel[i].insert(0, "#")
        tunnel[i].append("#")

    new_corners = [
        Coordinate(pos.x + shift_x + 1, pos.y + shift_y + 1) for pos in corners
    ]
    tunnel[new_corners[0].x][new_corners[0].y] = " "
    tunnel[new_corners[-1].x][new_corners[-1].y] = " "

    return tunnel, new_corners


def find_shortest_path_with_trace(
    tunnel: List[List[str]], start: Coordinate, end: Coordinate
) -> Tuple[int, List[Coordinate]]:
    if not tunnel or tunnel[start.x][start.y] == "#" or tunnel[end.x][end.y] == "#":
        return -1, []  # Start or end is blocked

    queue = deque([start])

    # Store visited coordinates and their parent to trace back
    visited = {start: None}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        pos = queue.popleft()

        # If we've reached the destination, backtrack to find the path
        if pos == end:
            path = []
            curr = end
            while curr is not None:
                path.append(curr)
                curr = visited[curr]
            path.reverse()

            # Distance is the number of nodes in the path
            return len(path), path

        for dr, dc in directions:
            new_pos = Coordinate(pos.x + dr, pos.y + dc)

            if tunnel[new_pos.x][new_pos.y] == " " and new_pos not in visited:
                visited[new_pos] = pos
                queue.append(new_pos)

    return -1, []  # No path found


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
part2()
# part3()
