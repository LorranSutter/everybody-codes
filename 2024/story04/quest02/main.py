import os
from typing import Dict, Tuple, Set

from utils.timer import timer
from utils.utils import tcolors

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
- This is a flood fill over the reachable squares. We keep two sets: `beetles` with everything seen
  so far, and `current_beetles`, the frontier we still need to expand. Each round, for every square in
  the frontier we take the midpoint towards all three beacons; any result that's new goes into
  `beetles` and into the next frontier. When the frontier comes up empty, every reachable square has
  been found.
- Expanding only the frontier (not the whole set) each round is what keeps this fast — a square is
  processed once, right after it's discovered.
- Then run the same firefly calculation as part 2 to get the final answer.
"""


@timer
def part1(plot=False):
    start, beacons, moves = parse_file("input01.txt")

    beetles = {start}
    pos = start
    for move in moves:
        pos = midpoint(beacons[move], pos)
        beetles.add(pos)

    if plot:
        plot_sky(beetles)

    print(f"Illuminated squares: {len(beetles)}")


@timer
def part2(plot=False):
    start, beacons, moves = parse_file("input02.txt")

    beetles = {start}
    pos = start
    for move in moves:
        pos = midpoint(beacons[move], pos)
        beetles.add(pos)

    fireflies = calculate_fireflies(beetles)

    if plot:
        plot_sky(beetles, fireflies)

    print(f"Number of fireflies: {len(fireflies)}")


@timer
def part3(plot=False):
    start, beacons, _ = parse_file("input03.txt")
    beacons = beacons.values()

    beetles = {start}
    current_beetles = {start}
    while current_beetles:
        new_beetles = set()
        for beetle in current_beetles:
            for b in beacons:
                p = midpoint(b, beetle)
                if p not in beetles:
                    beetles.add(p)
                    new_beetles.add(p)
        current_beetles = new_beetles

    fireflies = calculate_fireflies(beetles)

    if plot:
        plot_sky(beetles)

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


def plot_sky(
    beetles: Set[Tuple[int, int]],
    fireflies: Set[Tuple[int, int]] = frozenset(),
):
    """Print the sky to the terminal, in the style of the puzzle description.

    Beetles are drawn as a green X, fireflies as a yellow F, dark squares as a dot.
    Y grows upward, so rows are printed from the highest Y down to the lowest.
    """
    points = beetles | fireflies
    min_x = min(x for x, _ in points)
    max_x = max(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)

    for y in range(max_y, min_y - 1, -1):
        row = []
        for x in range(min_x, max_x + 1):
            if (x, y) in beetles:
                row.append(f"{tcolors.GREEN}X{tcolors.RESET}")
            elif (x, y) in fireflies:
                row.append(f"{tcolors.YELLOW}F{tcolors.RESET}")
            else:
                row.append(".")
        print("".join(row))


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
