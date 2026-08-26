import os
from typing import List
from itertools import cycle

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
    dancers = parse_file("input01.txt")
    size = len(dancers)

    rounds = 10
    for i in cycle(range(len(dancers))):
        if rounds <= 0:
            break

        idx = dancers[i][0]
        dancers[i].pop(0)
        dancers[(i + 1) % size].insert(idx - 1, idx)

        rounds -= 1

    shouted = sum((dancers[i][0] * 10 ** (size - i - 1) for i in range(size)))

    print(f"Number shouted: {shouted}")


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


def parse_file(file_name: str) -> List[List[int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    dancers = []
    with open(abs_file_path, "r") as f:
        data = []
        for line in f:
            data.append(list(map(int, line.split(" "))))

        # Transpose dancers matrix
        dancers = [list(row) for row in zip(*data)]

    return dancers


part1()
part2()
# part3()
