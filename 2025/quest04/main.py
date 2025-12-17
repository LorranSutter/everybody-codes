import os
import math
from typing import Tuple

"""
Preprocessing:
- Read the input file and split it into a list of integers.
- Gear rotation logic:
    - The number of rotations a gear makes depends on the number of teeth it has and the number o teeth of the previous gear.
    - We can simplify this logic just calculating the ratio of the number of teeth of two gears.

Part 1:
- Following the same ratio logic, we can calculate the ratio between the first and last gears.
- The new ratio will be a product between the current ratio and the previous ratio.
- The number of turns of the last gear is then the product of the new ratio and the given number of turns of the first gear.

Part 2:
- Similar to part 1, but we need to calculate the number of turns of the first gear instead.
- So instead of calculating the product, we calculate the ceiling of the quotient.
- The ceiling is needed to find the exact number of complete turns.

Part 3:
- Here we use another property of gears:
    - If two gears share the same shaft, the number of turns of both gears is the same.
- We have gear 1 (g1) and gear 2 (g2) sharing the same shaft:
    - g1 is conected to the last gear
    - g2 is connected to the next gear
    - If the last set has just one gear, we use this last gear to calculate the ratio with g1
    - Otherwise, we use he second gear to calculate the ration, using g1 and g2
- We follow the same logic as part 1 and 2 to calculate the number of turns of the last gear with the modification mentioned above.
"""


def part1():
    teeth_list = parse_file("input01.txt")
    gear_1_turns = 2025

    ratio = 1
    for i in range(len(teeth_list) - 1):
        ratio *= teeth_list[i] / teeth_list[i + 1]

    print("Number of turns of the last gear:", int(ratio * gear_1_turns))


def part2():
    teeth_list = parse_file("input02.txt")
    last_gear_turns = 10000000000000

    ratio = 1
    for i in range(len(teeth_list) - 1):
        ratio *= teeth_list[i] / teeth_list[i + 1]

    print("Number of turns of the first gear:", math.ceil(last_gear_turns / ratio))


def part3():
    teeth_list = parse_file_3("input03.txt")
    gear_1_turns = 100

    ratio = 1
    for i in range(len(teeth_list) - 1):
        if len(teeth_list[i]) == 1:
            ratio *= teeth_list[i][0] / teeth_list[i + 1][0]
        else:
            ratio *= teeth_list[i][1] / teeth_list[i + 1][0]

    print("Number of turns of the last gear:", int(ratio * gear_1_turns))


def parse_file(file_name: str) -> Tuple[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    teeth_list = tuple()
    with open(abs_file_path) as f:
        teeth_list = tuple([int(line.strip()) for line in f])

    return teeth_list


def parse_file_3(file_name: str) -> Tuple[Tuple[int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    teeth_list = list()
    with open(abs_file_path) as f:
        teeth_list = tuple([tuple(map(int,line.strip().split("|"))) for line in f])

    return teeth_list


part3()
