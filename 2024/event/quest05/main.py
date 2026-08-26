import os
from typing import List
from itertools import cycle
from collections import Counter

from utils.timer import timer

"""
Preprocessing:
-

Part 1:
-

Part 2:
- Initially I thought I could find a cycle. When I repeated shout
  is found for the first time, it means it is the start of a cycle.
  So the result would be just multiplying 2024 by the difference between
  the current round and the first time this shout appeared. However,
  it just works for small inputs like the sample 2. But for bigger
  inputs, it is likely to be two equal shouts with different grid
  configuration.

Part 3:
-
"""


class Dancers:
    def __init__(self, dancers: List[List[int]]):
        self.dancers = dancers
        self.size = len(dancers)

    def dance(self, col: int):
        idx = self.dancers[col][0]
        self.dancers[col].pop(0)
        target_col = self.dancers[(col + 1) % self.size]
        position = (idx - 1) % (2 * len(target_col))
        if position >= len(target_col):
            position = 2 * len(target_col) - position
        target_col.insert(position, idx)

    def shout(self):
        return int("".join(str(self.dancers[i][0]) for i in range(self.size)))


@timer
def part1():
    dancers = parse_file("input01.txt")
    dancers = Dancers(dancers)

    rounds = 10
    for i in cycle(range(dancers.size)):
        if rounds <= 0:
            break

        dancers.dance(i)
        rounds -= 1

    shouted = dancers.shout()
    print(f"Number shouted: {shouted}")


@timer
def part2():
    dancers = parse_file("input02.txt")
    dancers = Dancers(dancers)

    rounds = 0
    target_repeats = 2024
    repeated_shouts = {}
    shouts_count = Counter()
    for i in cycle(range(dancers.size)):
        dancers.dance(i)

        shouted = dancers.shout()
        repeated_shouts[shouted] = rounds
        shouts_count[shouted] += 1
        rounds += 1
        if shouts_count[shouted] == target_repeats:
            break

    result = rounds * shouted
    print(f"Result after {target_repeats} repeats: {result}")


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
