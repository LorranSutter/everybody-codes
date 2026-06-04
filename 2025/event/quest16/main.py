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
    spells = parse_file("input01.txt")
    wall_size = 90

    total = calc_blocks(spells, wall_size)

    print(f"Total blocks need to build the wall: {total}")


@timer
def part2():
    blocks = parse_file("input02.txt")
    wall_size = len(blocks)

    spells = calc_spells(blocks, wall_size)

    print(f"Spells used: {spells}")
    print(f"Product of spells that generated the wall: {math.prod(spells)}")


@timer
def part3():
    blocks = parse_file("input03.txt")
    wall_size = len(blocks)
    num_blocks = 202520252025000

    spells = calc_spells(blocks, wall_size)
    print(f"Spells used: {spells}")

    K = sum(1 / spell for spell in spells)

    wall_size = int(num_blocks / K)
    while calc_blocks(spells, wall_size + 1) <= num_blocks:
        wall_size += 1

    print(f"Number of wall colums: {wall_size}")


def calc_blocks(spells: List[int], wall_size: int) -> int:
    return sum(wall_size // spell for spell in spells)


def calc_spells(blocks: List[int], wall_size: int) -> List[int]:
    spells = []
    for i, block in enumerate(blocks, 1):
        if block > 0:
            for j in range(i - 1, wall_size, i):
                blocks[j] -= 1
            spells.append(i)

    return spells


def parse_file(file_name: str) -> List[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    with open(abs_file_path, "r") as f:
        return list(map(int, f.read().strip().split(",")))


part1()
part2()
part3()
