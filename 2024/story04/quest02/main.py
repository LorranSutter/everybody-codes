import os
from typing import Dict, Tuple, Set

from utils.timer import timer

"""
Preprocessing:
- Read the input file and return three things: the starting point, a dict of beacon positions keyed by
  letter, and the string of moves.

Part 1:
- Straightforward simulation. Iterate over each move and take the midpoint between the swarm's current
  position and the beacon named by that move. The midpoint uses floor division on each coordinate
  separately, which is exactly the "round fractions down" rule from the description.
- We keep every illuminated square in a set (seeded with START), so squares visited twice don't get
  double-counted. The answer is the size of that set.

Part 2:
- The first half is exactly part 1: simulate the moves and collect the illuminated squares.
- The second half places the fireflies. For every illuminated square we look at its four neighbours
  (up, down, left, right) and add a firefly there, unless that square is already a beetle square or
  already has a firefly. The answer is the number of fireflies.

Part 3:
- There's no MOVES sequence now: the next beacon is chosen at random, so we want every square that
  could ever be illuminated by some sequence of choices.
- I went with a brute-forcy fixpoint. Each round, for every beetle square found so far, take the
  midpoint towards every one of the three beacons and add the results back into the set. Stop once a
  full round doesn't grow the set any more.
- Then run the same firefly calculation as part 2 to get the final answer.
- Obs: this recomputes the same midpoints many times over, since it re-expands every square every
  round. A better way would be some recursive approach that only follows the squares added last round.
"""


@timer
def part1():
    start, beacons, moves = parse_file("input01.txt")

    beetles = set([start])
    pos = start
    for move in moves:
        pos = midpoint(beacons[move], pos)
        beetles.add(pos)

    print(f"Illuminated squares: {len(beetles)}")


@timer
def part2():
    start, beacons, moves = parse_file("input02.txt")

    beetles = set([start])
    pos = start
    for move in moves:
        pos = midpoint(beacons[move], pos)
        beetles.add(pos)

    fireflies = calculate_fireflies(beetles)

    print(f"Number of fireflies: {len(fireflies)}")


@timer
def part3():
    start, beacons, _ = parse_file("input03.txt")

    beetles = set([start])
    illuminated = 0
    while True:
        for beetle in beetles.copy():
            for b in beacons.values():
                beetles.add(midpoint(b, beetle))
        if len(beetles) <= illuminated:
            break
        illuminated = len(beetles)

    fireflies = calculate_fireflies(beetles)

    print(f"Number of fireflies: {len(fireflies)}")


def midpoint(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)


def calculate_fireflies(beetles: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    fireflies = set()

    for bettle in beetles:
        for di, dj in directions:
            new_position = (bettle[0] + di, bettle[1] + dj)
            if new_position not in fireflies and new_position not in beetles:
                fireflies.add(new_position)

    return fireflies


def parse_file(
    file_name: str,
) -> Tuple[Tuple[int, int], Dict[str, Tuple[int, int]], str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    start = None
    beacons = {}
    moves = ""
    with open(abs_file_path, "r") as f:
        for line in f:
            line = line.strip().split("=")

            if line[0] == "START":
                start = tuple(eval(line[1]))
            elif line[0] == "MOVES":
                moves = line[1]
            else:
                beacons[line[0]] = tuple(eval(line[1]))

    return start, beacons, moves


part1()
part2()
part3()
