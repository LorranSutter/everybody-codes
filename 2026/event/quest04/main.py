import os
import re
from dataclasses import dataclass
from collections import defaultdict

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
class Result:
    ID: int
    quest: int
    part: int
    time: int


@timer
def part1():
    results = parse_file("input01.txt")

    checksums = defaultdict(int)
    for result in results:
        checksums[result.ID] += result.time

    checksums = sorted(checksums.values())
    total_checksum = sum(i * checksum for i, checksum in enumerate(checksums, 1))

    print(f"Total checksum: {total_checksum}")


@timer
def part2():
    results = parse_file("input02.txt")

    ranking = dict()
    for result in results:
        if result.ID not in ranking:
            ranking[result.ID] = [1, result.time]
        else:
            ranking[result.ID][0] += 1
            ranking[result.ID][1] += result.time

    ranking = sorted(ranking.values(), key=lambda item: (-item[0], item[1]))
    total_checksum = sum(i * rank[1] for i, rank in enumerate(ranking, 1))

    print(f"Total checksum: {total_checksum}")


def parse_file(file_name: str) -> list[Result]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    results = []
    with open(abs_file_path, "r") as f:
        for line in f:
            line = re.findall(
                r"id=(\d+)\squest=(\d+)\spart=(\d+)\stime=(\d+)", line.strip()
            )[0]
            ID, quest, part, time = map(int, line)
            results.append(Result(ID, quest, part, time))
    return results


part1()
part2()
