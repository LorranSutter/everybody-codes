import os
from typing import List, Tuple
from functools import cmp_to_key
from dataclasses import dataclass

from utils.timer import timer

"""
Preprocessing:
- Part 1: Read the input file and parse into a list numbers and a sword ID.
- Part 2 and 3: Read the input file and parse each row into a list of numbers. Also return the list of sword IDs.
- We have a function to evaluate the a sword
    - It creates a list of Segment objects from the list of numbers.
    - It calculates the quality of the sword by concatenating the middle each segment.
    - It returns the Sword object with its sword Id, quality and segments.

Part 1:
- We just execute the evaluate_sword function once and return the quality of the sword.

Part 2:
- We execute the evaluate_sword function for all the swords.
- We return the difference between the highest and lowest quality swords.

Part 3:
- We also execute the evaluate_sword function for all the swords.
- We sort the Sword objects using a custom comparison function compare_swords.
- We calculate and return the checksum of the swords.
"""


@dataclass
class Segment:
    left: int = None
    middle: int = None
    right: int = None


@dataclass
class Sword:
    sword_id: int = None
    quality: int = None
    segments: List[Segment] = None


@timer
def part1():
    _, nums = parse_file_1("input01.txt")

    sword = evaluate_sword(nums)

    print("Quality of the sword:", sword.quality)


@timer
def part2():
    _, nums_list = parse_file_2("input02.txt")

    min_quality = float("inf")
    max_quality = float("-inf")
    for nums in nums_list:
        sword = evaluate_sword(nums)
        min_quality = min(min_quality, sword.quality)
        max_quality = max(max_quality, sword.quality)

    print(
        "Difference between the highest and lowest quality swords:",
        max_quality - min_quality,
    )


@timer
def part3():
    sword_ids, nums_list = parse_file_2("input03.txt")

    swords = [None for _ in range(len(sword_ids))]
    for i in range(len(sword_ids)):
        swords[i] = evaluate_sword(nums_list[i], sword_ids[i])

    swords.sort(key=cmp_to_key(compare_swords), reverse=True)

    checksum = sum([i * s.sword_id for i, s in enumerate(swords, 1)])

    print("Checksum of the swords:", checksum)


def evaluate_sword(nums: Tuple[int], sword_id: int = None) -> Sword:
    segments = [Segment()]
    quality = ""
    for num in nums:
        num_placed = False
        for segment in segments:
            if segment.middle is None:
                quality += str(num)
                segment.middle = num
                num_placed = True
                break
            if segment.left is None and num < segment.middle:
                segment.left = num
                num_placed = True
                break
            if segment.right is None and segment.middle < num:
                segment.right = num
                num_placed = True
                break

        if not num_placed:
            quality += str(num)
            new_segment = Segment(middle=num)
            segments.append(new_segment)

    return Sword(sword_id, int(quality), segments)


def compare_swords(s1: Sword, s2: Sword) -> int:
    if s1.quality > s2.quality:
        return 1
    elif s1.quality < s2.quality:
        return -1

    # The swords with same quality will have the same amount of segments
    for i in range(len(s1.segments)):
        segment1 = calculate_segment_numbers(s1.segments[i])
        segment2 = calculate_segment_numbers(s2.segments[i])

        if segment1 > segment2:
            return 1
        elif segment1 < segment2:
            return -1

    if s1.sword_id > s2.sword_id:
        return 1
    return -1


def calculate_segment_numbers(segment: Segment) -> int:
    num = ""

    if segment.left is not None:
        num += str(segment.left)
    if segment.middle is not None:
        num += str(segment.middle)
    if segment.right is not None:
        num += str(segment.right)

    return int(num)


def parse_file_1(file_name: str) -> Tuple[int, Tuple[int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    sword_id = 0
    nums = tuple()
    with open(abs_file_path) as f:
        sword_id, nums = f.readline().strip().split(":")
        nums = tuple(map(int, nums.split(",")))

    return sword_id, nums


def parse_file_2(file_name: str) -> Tuple[List[int], List[Tuple[int]]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    sword_ids = []
    nums_list = list()
    with open(abs_file_path) as f:
        for line in f:
            sword_id, nums = line.strip().split(":")
            sword_ids.append(int(sword_id))
            nums_list.append(tuple(map(int, nums.split(","))))

    return sword_ids, nums_list


part3()
