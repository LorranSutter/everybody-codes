import os
from dataclasses import dataclass
from typing import Tuple

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


@dataclass
class Thread:
    start: int
    end: int


@timer
def part1():
    nails = parse_file("input01.txt")
    half_len_nails = max(nails) // 2

    count_center = 0
    for i in range(len(nails) - 1):
        if abs(nails[i] - nails[i + 1]) == half_len_nails:
            count_center += 1

    print("Number of times a thread passes through center:", count_center)


@timer
def part2():
    # TODO: Implement part 2
    nails = parse_file("input_sample02.txt")
    print(nails)

    intersections = 0
    for i in range(len(nails) - 1):
        for j in range(i - 1, -1, -1):
            print(nails[i : i + 2], nails[j : j + 2])
            t1 = Thread(nails[i], nails[i + 1])
            t2 = Thread(nails[j], nails[j + 1])
            if intersect(t1, t2):
                print("Intersected")
                intersections += 1

    print("Total number of knots:", intersections)


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file("input_sample03.txt")
    pass


def intersect(t1: Thread, t2: Thread) -> bool:
    print(t1, t2)
    if (
        t1.start == t2.start
        or t1.end == t2.end
        or t1.start == t2.end
        or t1.end == t2.start
    ):
        print(t1, t2, "here1")
        return False

    # if t1.start > t1.end:
    #     t1 = Thread(t1.end, t1.start)
    # if t2.start > t2.end:
    #     t2 = Thread(t2.end, t2.start)

    if t1.start < t2.start < t1.end and t2.end < t2.end < t1.start:
        print(t1, t2, "here2")
        return True
    if t2.start < t1.start < t2.end and t2.end < t1.end < t2.start:
        print(t1, t2, "here3")
        return True
    if t1.end < t2.start < t1.start and t1.start < t2.end < t1.end:
        print(t1, t2, "here4")
        return True
    print(t1, t2, "here4")
    return False


def parse_file(file_name: str) -> Tuple[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    nails = []
    with open(abs_file_path, "r") as f:
        nails = tuple(map(int, f.readline().strip().split(",")))
    return nails


# part1()
part2()
# part3()
