import os
from typing import Tuple

from utils.timer import timer

"""
Preprocessing:
- For part 1, we need to read the input file and parse the numbers into a list.
- For parts 2 and 3, we need to read the input file and parse the ranges into a list of tuples.

Part 1:
- The idea here is to build the wheel first, then rotate it according to the given turns.
- We initialize the wheel with the number 1, then we add the numbers that goes on the right, then on the left.
- After the given number of turns, we find the value of the wheel at the given position.
    - On the right, we get every two the numbers from the left to the right
    - On the left, we get every two the numbers from the right to the left
- To calculate the final position, we just need to take the modulo of the total number of turns by the total numbers in the wheel.

Part 2:
- Same as part 1, but instead of adding the numbers directly, we add the numbers in the given ranges.

Part 3:
- Same as part 2, but with a much larger number of turns.
"""


@timer
def part1():
    nums = parse_file_1("input01.txt")

    turns = 2025
    total_nums = len(nums) + 1
    wheel = [1]

    for i in range(0, total_nums - 1, 2):
        wheel.append(nums[i])
    for i in range(total_nums - 2, 0, -2):
        wheel.append(nums[i])

    print(f"After {turns} turns, the value of the wheel is: {wheel[turns%total_nums]}")


@timer
def part2():
    ranges = parse_file_2("input02.txt")

    turns = 20252025
    total_nums = 1
    wheel = [1]

    for i in range(0, len(ranges), 2):
        for num in range(ranges[i][0], ranges[i][1] + 1):
            wheel.append(num)
            total_nums += 1

    len_range = len(ranges) - 1 if len(ranges) % 2 == 0 else len(ranges) - 2
    for i in range(len_range, 0, -2):
        for num in range(ranges[i][1], ranges[i][0] - 1, -1):
            wheel.append(num)
            total_nums += 1

    print(f"After {turns} turns, the value of the wheel is: {wheel[turns%total_nums]}")


@timer
def part3():
    ranges = parse_file_2("input03.txt")    

    turns = 202520252025
    total_nums = 1
    wheel = [1]

    for i in range(0, len(ranges), 2):
        for num in range(ranges[i][0], ranges[i][1] + 1):
            wheel.append(num)
            total_nums += 1    

    len_range = len(ranges) - 1 if len(ranges) % 2 == 0 else len(ranges) - 2
    for i in range(len_range, 0, -2):
        for num in range(ranges[i][1], ranges[i][0] - 1, -1):
            wheel.append(num)
            total_nums += 1

    print(f"After {turns} turns, the value of the wheel is: {wheel[turns%total_nums]}")


def parse_file_1(file_name: str) -> Tuple[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    nums = []
    with open(abs_file_path, "r") as f:
        nums = [int(line.strip()) for line in f]
    return nums


def parse_file_2(file_name: str) -> Tuple[Tuple[int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    ranges = []
    with open(abs_file_path, "r") as f:
        ranges = [tuple(map(int, line.strip().split("-"))) for line in f]
    return ranges


part1()
part2()
part3()
