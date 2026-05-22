import os
from typing import List, Tuple
from itertools import combinations

from utils.timer import timer
from utils.utils import tcolors

"""
Preprocessing:
- Read the input file and parse into a list of integers.

Part 1:
- The trick here is realizing that for a thread to pass though the center, the difference
  between two nail positions is half the amount of nails of the nails.
  E.g.: Length of nails = 10, half of 10 = 5
        Thread 1: (2, 8) = 6 -> don't pass through center
        Thread 2: (7, 2) = 5 -> pass through center
- Then, we just have to iterate through the list of nails and count the pairs that satisfy the condition.

Part 2:
- A brute force approach that checks if a new thread intersects the existing previous threads.
- We can see the circle as 1D line of segments
- The goal here is just find threads that overlaps each other, but excluding shared endpoints and containment

           // *---------* 
  Not Good -                      
           \\ *--------------* \\ 
                                - Good
         *--------------*      // 
    |----|----|----|----|----|----|----|
    1    2    3    4    5   6     7    8

- Then, we just have to count the total number of knots and return the result.

Part 3:
- Pretty similar to part 2, but instead of checking only existing threads, we need to check all possible pairs of nails.
- We keep track the segment that made the most cuts and return the result.
- One tricky thing is that, the cut could be one of the exiting threads.
  In this case, we have to add 1 to the count, since this thread will also be cut and the overlapping function does not consider this case.
"""


@timer
def part1():
    nails = parse_file("input01.txt")
    half_len_nails = max(nails) // 2

    count_center = 0
    for i in range(len(nails) - 1):
        if abs(nails[i] - nails[i + 1]) == half_len_nails:
            count_center += 1

    print(
        f"Number of times a thread passes through center: {tcolors.GREEN}{count_center}{tcolors.RESET}"
    )


@timer
def part2():
    nails = parse_file("input02.txt")

    intersections = 0
    for i in range(len(nails) - 1):
        print(
            f"Checking thread {tcolors.YELLOW}{i + 1}/{len(nails) - 1}{tcolors.RESET}",
            end="\r",
        )
        for j in range(i - 1, -1, -1):
            t1 = sorted([nails[i], nails[i + 1]])
            t2 = sorted([nails[j], nails[j + 1]])
            if overlapping(t1, t2):
                intersections += 1

    print(f"\nTotal number of knots: {tcolors.GREEN}{intersections}{tcolors.RESET}")


@timer
def part3():
    nails = parse_file("input03.txt")

    threads = [sorted([nails[i], nails[i + 1]]) for i in range(len(nails) - 1)]
    cuts = combinations([i for i in range(1, max(nails) + 1)], 2)

    max_cuts = 0
    best_cut = ()
    for cut in cuts:
        print(
            f"Checking cut {tcolors.YELLOW}{cut[0]+1}/{max(nails)}{tcolors.RESET}",
            end="\r",
        )
        num_cuts = 0
        for thread in threads:
            if overlapping(thread, cut):
                num_cuts += 1

        if num_cuts > max_cuts:
            best_cut = cut
            max_cuts = num_cuts

    # Check if best cut is also a thread
    if list(best_cut) in threads:
        max_cuts += 1

    print(
        f"\nBest cut: {tcolors.GREEN}{best_cut}{tcolors.RESET}, Max number of cuts: {tcolors.GREEN}{max_cuts}{tcolors.RESET}"
    )


def overlapping(t1: List[int], t2: List[int]) -> bool:
    """Check if two threads overlap (excluding shared endpoints and containment)."""

    # Threads share an endpoint
    if t1[0] == t2[0] or t1[1] == t2[1] or t1[0] == t2[1] or t1[1] == t2[0]:
        return False

    # Threads overlap
    if max(t1[0], t2[0]) <= min(t1[1], t2[1]):
        # t2 contains t1
        if t1[0] > t2[0] and t1[1] < t2[1]:
            return False

        # t1 contains t2
        if t2[0] > t1[0] and t2[1] < t1[1]:
            return False

        return True

    # Threads do not overlap
    return False


def parse_file(file_name: str) -> Tuple[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    nails = []
    with open(abs_file_path, "r") as f:
        nails = tuple(map(int, f.readline().strip().split(",")))
    return nails


part1()
part2()
part3()
