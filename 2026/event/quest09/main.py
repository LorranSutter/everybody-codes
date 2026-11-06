import os
import re
from dataclasses import dataclass

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


@dataclass(frozen=True)
class Plant:
    ID: int
    growth: int
    limit: int


@timer
def part1():
    plants = parse_file("input01.txt")

    total_seconds = 0
    for plant in plants:
        branches = [0]
        elements = 0

        while elements < plant.limit:
            new_branches = []
            for i in range(len(branches)):
                branches[i] += 1
                elements += 1
                if branches[i] >= plant.growth:
                    elements += 1
                    branches[i] = plant.growth // 2
                    new_branches.append(plant.growth // 2)
                    new_branches.append(1)

            branches.extend(new_branches)
            total_seconds += 1

    print(f"Growth time: {total_seconds}")


@timer
def part2():
    plants = parse_file("input02.txt")

    total_seconds = 0
    for plant in plants:
        branching_points = 0
        branches = [0]
        elements = 0

        while branching_points + 1 < plant.limit:
            new_branches = []
            for i in range(len(branches)):
                branches[i] += 1
                elements += 1
                if branches[i] >= plant.growth:
                    elements += 1
                    branching_points += 1
                    branches[i] = plant.growth // 2
                    new_branches.append(plant.growth // 2)
                    new_branches.append(1)

            branches.extend(new_branches)
            total_seconds += 1

    print(f"Growth time: {total_seconds}")


@timer
def part3():
    # TODO: Implement part 3
    pass


def parse_file(file_name: str) -> list[Plant]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    plants = []
    with open(abs_file_path, "r") as f:
        for line in f:
            line = re.findall(r"id=(\d+),\sgrowth=(\d+),\slimit=(\d+)", line.strip())[0]
            plants.append(Plant(*map(int, line)))
    return plants


part1()
part2()
# part3()
