import os
import math
from typing import List

from utils.timer import timer

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
    pattern = parse_file("input01.txt")
    wall_size = 90

    total = sum(wall_size // spell for spell in pattern)

    print(f"Total blocks need to build the wall: {total}")


@timer
def part2():
    blocks = parse_file("input02.txt")
    wall_size = len(blocks)

    spells = []
    for i, block in enumerate(blocks, 1):
        if block > 0:
            for j in range(i - 1, wall_size, i):
                blocks[j] -= 1
            spells.append(i)

    print(f"Spells used: {spells}")
    print(f"Product of spells that generated the wall: {math.prod(spells)}")


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file("input_sample03.txt")
    pass


def parse_file(file_name: str) -> List[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    with open(abs_file_path, "r") as f:
        return list(map(int, f.read().strip().split(",")))


part1()
part2()
# part3()
