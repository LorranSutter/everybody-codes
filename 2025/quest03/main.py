import os
from typing import List

from utils.timer import timer

"""
Preprocessing:
- Read the input file and split it into a list of integers.

Part 1:
- Since we can just pack crates that are smaller than the previous crate, we just create a set to remove the duplicates.
- The answer is the sum of the elements in the set.

Part 2:
- Similar to part 1, but we just need the first 20 crates.
- For that, we just have to sort the crates and take the first 20.

Part 3:
- For this one, we don't worry about duplicates. In fact, we need them.
- Since there can be only one crate type per set, we know that each set will have unique creates.
- The maximum amount of sets depends on the most frequent crate type.
- We just count the frequency of each crate and find the most frequent crate type.
"""


@timer
def part1():
    crates = parse_file("input01.txt")
    crates = set(crates)

    print("Largest possible set:", sum(crates))


@timer
def part2():
    crates = parse_file("input02.txt")
    crates = list(set(crates))
    crates.sort()

    print("Smallest possible set:", sum(crates[:20]))


@timer
def part3():
    crates = parse_file("input03.txt")

    count = dict()
    most_common_crate_count = 0
    for crate in crates:
        if crate not in count:
            count[crate] = 0
        count[crate] += 1

        if count[crate] > most_common_crate_count:
            most_common_crate_count = count[crate]

    print("Total amount of sets:", most_common_crate_count)


def parse_file(file_name: str) -> List[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    crates = list()
    with open(abs_file_path) as f:
        crates = list(map(int, f.readline().strip().split(",")))

    return crates


part1()
