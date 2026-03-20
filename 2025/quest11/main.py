import os
from typing import List

from utils.timer import timer

"""
Preprocessing:
- Read the input file and make an array of integers from each line.

Part 1:
- Just a simple simulation of the problem description.

Part 2:
- Regular simulation of phase 1
- By the end of phase 1, the columns will be in ascending order.
- The columns are balanced when all columns have the same number of birds, which is the total number of birds divided by the number of columns.
- Then, for each column that has less birds than the balanced count, we calculate the difference and add it to the round count.
- The final result is the sum of rounds from phase 1 and phase 2.

Part 3:
- Same as part 2, but we can skip phase 1 since the input is already in ascending order.
"""


@timer
def part1():
    columns = parse_file("input01.txt")
    num_cols = len(columns)
    max_rounds = 10
    round = -1

    # Phase 1
    moved = True
    while moved:
        moved = False
        round += 1
        for i in range(num_cols - 1):
            if columns[i] > columns[i + 1]:
                columns[i] -= 1
                columns[i + 1] += 1
                moved = True

    # Phase 2
    while round < max_rounds:
        round += 1
        for i in range(num_cols - 1):
            if columns[i] < columns[i + 1]:
                columns[i] += 1
                columns[i + 1] -= 1

    checksum = sum([(i + 1) * columns[i] for i in range(num_cols)])
    print(f"Flock checksum after {round} rounds: {checksum}")


@timer
def part2():
    columns = parse_file("input02.txt")
    num_cols = len(columns)
    round = -1

    # Phase 1
    moved = True
    while moved:
        moved = False
        round += 1
        for i in range(num_cols - 1):
            if columns[i] > columns[i + 1]:
                columns[i] -= 1
                columns[i + 1] += 1
                moved = True

    # Phase 2
    each_col_count = sum(columns) // num_cols

    for col in columns:
        if col < each_col_count:
            round += each_col_count - col

    print("Number of rounds until balance: ", round)


@timer
def part3():
    columns = parse_file("input03.txt")

    # Phase 1
    # Skip phase 1 since the input is already in ascending order

    # Phase 2
    each_col_count = sum(columns) // len(columns)

    round = 0
    for col in columns:
        if col < each_col_count:
            round += each_col_count - col

    print("Number of rounds until balance: ", round)


def parse_file(file_name: str) -> List[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    lines = []
    with open(abs_file_path, "r") as f:
        for line in f:
            lines.append(int(line.strip()))
    return lines


# part1()
# part2()
part3()
