import os
from typing import List, Tuple

from utils.timer import timer
from utils.utils import tcolors

"""
Preprocessing:
- Read the input file and parse the floor into a 2D array of integers.
- Optionally, add a border with '.' tile around the floor to simplify the calculation.

Part 1:
- Straightforward simulation of something similar to Game of Life for 10 cycles.
- For each cycle, we iter over the floor and apply the rules to determine the next state of each tile.
- We count the number of active tiles at the end of each cycle.

Part 2:
- Same as part 1, but with 2025 cycles.

Part 3:
- After careful observation, we can find that the floor will eventually start repeating the same configuration, reaching a stable state.
- So, we can perform the simulation until we find a repeating configuration.
- During the simulation, we check if the pattern is found in the floor and count the number of active tiles when this is true.
- Knowing the number of cycles to reach the stable state, we can calculate how many times the pattern will be found in the total number of cycles and sum up the active tiles accordingly.
"""


@timer
def part1():
    floor = parse_file("input01.txt", with_border=True)

    num_cycles = 10
    total_active_tiles = 0

    for _ in range(num_cycles):
        floor, num_active_tiles = next_round(floor)
        total_active_tiles += num_active_tiles
        print(f"Number of active tiles after one cycle: {num_active_tiles}")

    print_floor(floor)
    print(
        f"Total number of active tiles after {num_cycles} cycles: {total_active_tiles}"
    )


@timer
def part2():
    floor = parse_file("input02.txt", with_border=True)

    num_cycles = 2025
    total_active_tiles = 0

    for _ in range(num_cycles):
        floor, num_active_tiles = next_round(floor)
        total_active_tiles += num_active_tiles
        print(f"Number of active tiles after one cycle: {num_active_tiles}")

    print_floor(floor)
    print(
        f"Total number of active tiles after {num_cycles} cycles: {total_active_tiles}"
    )


@timer
def part3():
    pattern = parse_file("input03.txt")

    total_num_cycles = 1000000000

    # Generate the filled floor with border
    size = (34, 34)
    floor = []
    for _ in range(size[0]):
        floor.append(["."] + ["#"] * size[1] + ["."])
    floor.insert(0, ["."] * len(floor[0]))
    floor.append(["."] * len(floor[0]))

    # Make one round to get a starting point (it will never get back to a fully filled floor)
    floor, num_active_tiles = next_round(floor)
    # Stores the starting point for comparison
    floor_first = floor.copy()

    title_count_map = {}
    stable_num_cycles = 0
    while True:
        stable_num_cycles += 1

        if contain_pattern(floor, pattern):
            title_count_map[stable_num_cycles] = num_active_tiles
            print(f"Found pattern after {stable_num_cycles} cycles")

        floor, num_active_tiles = next_round(floor)

        if is_equal(floor, floor_first):
            print(f"Reached stable state after {stable_num_cycles} cycles")
            break

    print()
    print("Title count map:", title_count_map)
    print(f"Total number of active tiles with pattern before stable state: {sum(title_count_map.values())}")

    # Calculate the total number of active tiles after total_num_cycles cycles
    num_active_tiles = total_num_cycles//stable_num_cycles * sum(title_count_map.values())

    # Since the total number of cycles is not a multiple of stable_num_cycles, we need to add the remaining cycles
    remaining_cycles = total_num_cycles % stable_num_cycles
    for key, value in title_count_map.items():
        if key <= remaining_cycles:
            num_active_tiles += value
    
    print(f"Total number of active tiles after {total_num_cycles} cycles: {num_active_tiles}")


def next_round(floor: List[List[str]]) -> Tuple[List[List[str]], int]:
    """
    Apply the rules to determine the next state of each tile and count the number of active tiles.
    """
    num_active_tiles = 0
    new_floor = [["." for _ in range(len(floor[0]))] for _ in range(len(floor))]

    for i in range(1, len(floor) - 1):
        for j in range(1, len(floor[0]) - 1):
            active_diag = sum(
                [
                    floor[i - 1][j - 1] == "#",
                    floor[i - 1][j + 1] == "#",
                    floor[i + 1][j - 1] == "#",
                    floor[i + 1][j + 1] == "#",
                ]
            )
            match floor[i][j]:
                case "#":
                    if active_diag % 2 != 0:
                        new_floor[i][j] = "#"
                        num_active_tiles += 1
                case ".":
                    if active_diag % 2 == 0:
                        new_floor[i][j] = "#"
                        num_active_tiles += 1

    return new_floor, num_active_tiles


def is_equal(floor1: List[List[int]], floor2: List[List[int]]) -> bool:
    for i in range(1, len(floor1) - 1):
        for j in range(1, len(floor1[0]) - 1):
            if floor1[i][j] != floor2[i][j]:
                return False
    return True


def contain_pattern(floor: List[List[int]], pattern: List[List[int]]) -> bool:
    """
    Check if the pattern is found in the floor.
    We consider that the pattern is found in the middle of the floor, not at the edges.
    """
    floor_size = (len(floor), len(floor[0]))
    pattern_size = (len(pattern), len(pattern[0]))

    if floor_size[0] < pattern_size[0] or floor_size[1] < pattern_size[1]:
        return False

    gap_x = (floor_size[0] - pattern_size[0]) // 2
    gap_y = (floor_size[1] - pattern_size[1]) // 2

    for i in range(gap_x, pattern_size[0] + gap_x):
        for j in range(gap_y, pattern_size[1] + gap_y):
            if floor[i][j] != pattern[i - gap_x][j - gap_y]:
                return False

    return True


def print_floor(floor: List[List[int]]) -> None:
    for i in range(len(floor)):
        for j in range(len(floor[0])):
            if floor[i][j] == "#":
                print(f"{tcolors.RED}#{tcolors.RESET}", end="")
            else:
                print(".", end="")
        print()


def parse_file(file_name: str, with_border: bool = False) -> List[List[str]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    floor = []
    with open(abs_file_path, "r") as f:
        for line in f:
            if with_border:
                floor.append(["."] + [tile for tile in line.strip()] + ["."])
            else:
                floor.append([tile for tile in line.strip()])

    if with_border:
        floor.insert(0, ["."] * len(floor[0]))
        floor.append(["."] * len(floor[0]))

    return floor


# part1()
# part2()
part3()
