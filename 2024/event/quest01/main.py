import os

from utils.timer import timer

"""
Part 1:
- Straightforward: sum up the potions needed per creature using a lookup table (`A` costs 0, `B` costs
  1, `C` costs 3).

Part 2:
- Creatures now come in pairs, and fighting alongside another creature costs 1 extra potion each. My
  first pass handled this by hand: check whether neither slot in the pair was an `x` placeholder, and
  if so, add 2 to the pair's total. That manual check is what part 3 generalizes.

Part 3:
- The insight is that we don't need to reason about pairs vs. triples as different cases at all — we
  just need to know how many real creatures are in a group, and `x` placeholders are the only thing
  standing in the way of that count. Strip them out, and the group size `n` tells you everything: each
  of the `n` creatures pays 1 extra potion per teammate, so the group's total surcharge is n * (n - 1).

Obs: This formula also happens to cover part 1 for free, since a "group" of size 1 gives n * (n - 1) = 0
     Which is why `calculate_potions()` is the same function for all three parts, called with groups of
     size 1, 2, and 3 respectively.
"""


@timer
def part1():
    creatures = parse_file("input01.txt")

    total_potions = 0
    for i in range(len(creatures)):
        total_potions += calculate_potions(creatures[i])

    print(f"Total potions: {total_potions}")


@timer
def part2():
    creatures = parse_file("input02.txt")

    total_potions = 0
    for i in range(0, len(creatures), 2):
        total_potions += calculate_potions(creatures[i : i + 2])

    print(f"Total potions: {total_potions}")


@timer
def part3():
    creatures = parse_file("input03.txt")

    total_potions = 0
    for i in range(0, len(creatures), 3):
        total_potions += calculate_potions(creatures[i : i + 3])

    print(f"Total potions: {total_potions}")


def calculate_potions(creatures: str) -> int:
    potions = {"x": 0, "A": 0, "B": 1, "C": 3, "D": 5}

    creatures = creatures.replace("x", "")
    size = len(creatures)

    creature_potions = sum(potions[c] for c in creatures)
    return creature_potions + size * (size - 1)


def parse_file(file_name: str) -> str:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    creatures = ""
    with open(abs_file_path, "r") as f:
        creatures = f.read().strip()
    return creatures


part1()
part2()
part3()
