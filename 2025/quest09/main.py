import os
from itertools import combinations
from dataclasses import dataclass
from typing import List, Tuple, Set

from utils.timer import timer

"""
Preprocessing:
- Read the input file and parse into a list of strings representing DNA sequences.

Part 1:
- Count the number of matching characters between the first and third DNA sequences, and between the second and third DNA sequences.
- Calculate the degree of similarity as the product of these two counts.

Part 2:
- We iterate over all possible combinations of sets of three DNA sequences.
- Since we don't know what DNA is the child in each set, we calculate the degree of similarity for all three possible parent-child combinations.
- We sum up all the similarity degrees calculated for each combination.

Part 3:
- First, we parse the input file and store the DNA sequences in a list of DNA objects.
- Then, we also generate all possible combinations of sets of three DNA sequences.
- Instead of calculating the degree of similarity, we check if one of the DNA sequences can be a child of the other two using the is_child function.
- If a valid, we create a new set containing the IDs of the three DNA sequences.
- We try to merge the new set with any existing sets. The merge occurs if the new set has at least one common DNA sequence with any existing set.
- After processing all combinations, we will have a list of sets. However, there still could be sets that can be merged.
- We call the merge_sets function to merge any sets that can be merged if they share at least one common DNA sequence.
- Finally, we find the largest set and calculate the sum of the IDs of the DNA sequences
"""


@dataclass
class DNA:
    id: int
    sequence: str


@timer
def part1():
    dnas = parse_file("input01.txt")

    matches1 = sum(1 for a, b in zip(dnas[0], dnas[2]) if a == b)
    matches2 = sum(1 for a, b in zip(dnas[1], dnas[2]) if a == b)

    print(f"Degree of similarity: {matches1*matches2}")


@timer
def part2():
    dnas = parse_file("input02.txt")

    similarity_degrees_sum = 0
    for dna1, dna2, dna3 in combinations(dnas, 3):
        similarity1 = calculate_matches(dna1, dna2, dna3)
        similarity2 = calculate_matches(dna1, dna3, dna2)
        similarity3 = calculate_matches(dna3, dna2, dna1)

        similarity_degrees_sum += similarity1 + similarity2 + similarity3

    print(f"Sum of similarity degrees: {similarity_degrees_sum}")


@timer
def part3():
    dnas = parse_file("input03.txt")
    dnas = [DNA(i, dna) for i, dna in enumerate(dnas, 1)]

    sets = []
    for dna1, dna2, dna3 in combinations(dnas, 3):
        if is_child(dna1.sequence, dna2.sequence, dna3.sequence):
            sets = merge_set(sets, {dna1.id, dna2.id, dna3.id})
            print(f"Total sets: {len(sets)}")
        elif is_child(dna1.sequence, dna3.sequence, dna2.sequence):
            sets = merge_set(sets, {dna1.id, dna3.id, dna2.id})
            print(f"Total sets: {len(sets)}")
        elif is_child(dna3.sequence, dna2.sequence, dna1.sequence):
            sets = merge_set(sets, {dna3.id, dna2.id, dna1.id})
            print(f"Total sets: {len(sets)}")

    print("Merging sets...")
    sets = merge_sets(sets)

    max_len = 0
    max_set = None
    for set in sets:
        if len(set) > max_len:
            max_len = len(set)
            max_set = set

    print(f"Sum of the scales of the largest family: {sum(max_set)}")


def calculate_matches(parent1: str, parent2: str, child: str) -> int:
    matches1, matches2 = 0, 0
    for p1, p2, c in zip(parent1, parent2, child):
        if c != p1 and c != p2:
            return 0
        if c == p1:
            matches1 += 1
        if c == p2:
            matches2 += 1

    return matches1 * matches2


def is_child(parent1: str, parent2: str, child: str) -> int:
    for p1, p2, c in zip(parent1, parent2, child):
        if c != p1 and c != p2:
            return False

    return True


def merge_set(sets: List[Set[int]], new_set: Set[int]) -> Set[int]:
    updated = False
    for set in sets:
        if set & new_set:
            set.update(new_set)
            updated = True

    if not updated:
        return sets + [new_set]

    return sets


def merge_sets(sets: List[Set[int]]) -> List[Set[int]]:
    if not sets:
        return []

    # Keep merging until no more merges are possible
    changed = True
    while changed:
        changed = False
        merged_sets = []
        skip_indices = set()

        for i in range(len(sets)):
            if i in skip_indices:
                continue

            current_set = sets[i].copy()

            # Try to merge with remaining sets
            for j in range(i + 1, len(sets)):
                if j in skip_indices:
                    continue

                # If sets share at least one element, merge them
                if current_set & sets[j]:
                    current_set.update(sets[j])
                    skip_indices.add(j)
                    changed = True

            merged_sets.append(current_set)

        sets = merged_sets

    return sets


def parse_file(file_name: str) -> Tuple[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    dnas = []
    with open(abs_file_path, "r") as f:
        for line in f:
            # Skip the first the id (e.g., "1:", "2:", "3:")
            dnas.append(line.strip().split(":")[1])
    return tuple(dnas)


part1()
part2()
part3()
