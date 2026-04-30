import os
from typing import Tuple

from utils.timer import timer

"""
Preprocessing:
- Read the input file and split it into a list of strings. Each string represents a person.

Part 1:
- We iterate through the list of people and count the number of mentors (A).
- Everytime we encounter a novice (a), we add the current number of mentors (A) to the pairs count.

Part 2:
- Same as part 1, but now we also count the number of mentors for each category (A, B, C).

Part 3:
- Instead of counting like part 1 and 2, we have to check the surroundings for each novice (a, b, c) within the distance limit.
    - We iterate through the list of people and call get_mentors for each novice.
    - Since the pattern repeats, we have to extend the pattern we iterate
    - For example:
        - Original pattern: AABCBABCABCabcabcABCCBAACBCa
        - Extended pattern:
                                                  N
            BCCBAACBCa AABCBABCABCabcabcABCCBAACBCa AABCBABCAB
                                        M....MM.... MM...M.... = 6
    - The get_mentors returns the number of mentors on the left, the right and the middle pattern
- After we have all the mentors on the left, the right and the middle for each category (A, B, C), we can calculate the total pairs
    - We can think of the calculation this way:
    - Initial pattern:       XXXXX
    - Extendend pattern: aaa XXXXX bbb 
    - Repeated pattern:      XXXXX bbb aaa XXXXX bbb aaa XXXXX
    - We can ignore the left and right extension for the first and last repeats
    - We can rewrite the repeated patterm this way:

        aaa XXXXX bbb aaa XXXXX bbb  ... XXXXX

    - The final formula then is:
      - mentors = mentors_left + mentors_middle + mentors_right
      - total = mentors * (repeats - 1) + mentors_middle

Note: Part 3 only works for inputs with size >= distance
"""


@timer
def part1():
    people = parse_file("input01.txt")

    mentors = 0
    pairs = 0
    for i in range(len(people)):
        if people[i] == "A":
            mentors += 1
        elif people[i] == "a":
            pairs += mentors

    print("Total number novice-mentor pairs in the sword fighting category:", pairs)


@timer
def part2():
    people = parse_file("input02.txt")

    mentors_A, mentors_B, mentors_C = 0, 0, 0
    pairs_A, pairs_B, pairs_C = 0, 0, 0
    for i in range(len(people)):
        if people[i] == "A":
            mentors_A += 1
        elif people[i] == "B":
            mentors_B += 1
        elif people[i] == "C":
            mentors_C += 1
        elif people[i] == "a":
            pairs_A += mentors_A
        elif people[i] == "b":
            pairs_B += mentors_B
        else:
            pairs_C += mentors_C

    print("Total number of novice-mentor pairs:", pairs_A + pairs_B + pairs_C)


@timer
def part3():
    people = parse_file("input03.txt")
    dist = 1000
    repeats = 1000
    extended_people = people[-dist:] + people + people[:dist]

    mentors_left = 0
    mentors_middle = 0
    mentors_right = 0
    for i in range(len(people)):
        if people[i].islower():
            m_l, m_m, m_r = get_mentors(
                people, extended_people, i, people[i].upper(), dist
            )
            mentors_left += m_l
            mentors_middle += m_m
            mentors_right += m_r

    mentors = mentors_left + mentors_middle + mentors_right

    print(
        "Total number of novice-mentor pairs:", mentors * (repeats - 1) + mentors_middle
    )


def get_mentors(
    people: Tuple[str], extended_people: Tuple[str], id: int, mentor: str, dist: int
) -> Tuple[int, int, int]:
    lower = id - dist
    higher = id + dist + 1

    lower_extended = -1
    if lower < 0:
        lower_extended = dist + lower
        lower = 0

    higher_extended = -1
    if higher >= len(people):
        higher_extended = higher + dist
        higher = len(people) - 1

    mentors_left = 0
    mentors_middle = 0
    mentors_right = 0
    if lower_extended > -1:
        for i in range(lower_extended, dist):
            if extended_people[i] == mentor:
                mentors_left += 1

    if higher_extended > -1:
        for i in range(len(people) + dist, higher_extended):
            if extended_people[i] == mentor:
                mentors_right += 1

    for i in range(lower, higher):
        if people[i] == mentor:
            mentors_middle += 1

    return mentors_left, mentors_middle, mentors_right


def parse_file(file_name: str) -> Tuple[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    people = tuple()
    with open(abs_file_path) as f:
        people = tuple([p for p in f.readline().strip()])

    return people


part3()
