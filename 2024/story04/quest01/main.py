import os
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt

from utils.timer import timer

"""
Part 1:
- Straight simulation of the rules, no real trick. The only nod to speed is keeping visited points in a
  set so the "have we been here?" check is O(1).
- A backward jump that fails turns into a forward jump of the same length, which is a net move of +jump
  from where we started. The code writes that as `current -= jump` and then, if that spot is bad,
  `current += 2 * jump`.
- Run every ornament, keep each final position, sum them.

Part 2:
- Same as part 1 with one extra rule: when the forward jump lands on a visited point, keep adding 1 until
  we hit an unvisited one (`while current in visited: current += 1`). Backward jumps are unchanged.
- Run every ornament, keep each final position, sum them.

Part 3:
- Now arcs must not cross. Three things get added:
  1. Store the intervals spanned by the arcs, split into two lists: arcs drawn below the number line and
     arcs drawn above it. Sides alternate (below, above, below, ...), and only two arcs on the same side
     can ever cross, so we only test a new arc against its own side.
  2. A crossing test between two arcs. Represent each arc by the sorted interval of its two endpoints.
     Two same-side arcs cross exactly when their intervals partially overlap - not disjoint, and not one
     nested inside the other:
         [0, 5] vs [3, 8]  ->  interleaved, they cross
         [0, 8] vs [3, 5]  ->  nested, the small arc sits under the big one, no crossing
         [0, 3] vs [5, 8]  ->  disjoint, no crossing
  3. The farthest point reached so far (`max_position`), used to decide when a jump is hopeless.
- Jump resolution (`resolve_jump`) keeps the same shape as before with the crossing test bolted on: try
  backward first (in range, unvisited, no crossing on this side), otherwise go forward, sliding the target
  past any visited or crossing spot.
- `max_position` is the stop condition for that forward slide. Once the target has been bumped more than 1
  past the farthest point we have ever reached, pushing it further only widens the arc over the same
  obstacles - there is no valid landing, so we skip this jump length entirely and move on to the next one.
- Run every ornament, keep each final position, sum them.
"""


@timer
def part1(plot: bool = False):
    ornaments = parse_file("input01.txt")

    sum_last_visited = 0
    for ornament in ornaments:
        current = 0
        visited = set([0])
        # True -> below, False -> above
        intervals = {True: [], False: []}
        below = True
        for jump in ornament:
            previous = current
            # Jump backwards
            current -= jump
            if current < 0 or current in visited:
                # Jump forwards
                current += 2 * jump
            visited.add(current)
            intervals[below].append(sorted((previous, current)))
            below = not below

        sum_last_visited += current

        if plot:
            plot_arcs(intervals[True], intervals[False])

    print(f"Sum of last visited: {sum_last_visited}")


@timer
def part2(plot: bool = False):
    ornaments = parse_file("input02.txt")

    sum_last_visited = 0
    for ornament in ornaments:
        current = 0
        visited = set([0])
        # True -> below, False -> above
        intervals = {True: [], False: []}
        below = True
        for jump in ornament:
            previous = current
            # Jump backwards
            current -= jump
            if current < 0 or current in visited:
                # Jump forwards
                current += 2 * jump
                while current in visited:
                    current += 1
            visited.add(current)
            intervals[below].append(sorted((previous, current)))
            below = not below

        sum_last_visited += current

        if plot:
            plot_arcs(intervals[True], intervals[False])

    print(f"Sum of last visited: {sum_last_visited}")


@timer
def part3(plot=False):
    ornaments = parse_file("input_sample03.txt")

    sum_last_visited = 0
    for ornament in ornaments:
        # True -> below, False -> above
        intervals = {True: [], False: []}
        current = 0
        max_position = 0
        below = True
        visited = set([0])

        for jump in ornament:
            landing = resolve_jump(
                current, jump, visited, intervals[below], max_position
            )
            # No jump is possible: skip this ornament's jump entirely
            if landing is None:
                continue

            intervals[below].append(sorted((current, landing)))
            current = landing
            max_position = max(max_position, current)
            visited.add(current)
            below = not below

        sum_last_visited += current

        if plot:
            plot_arcs(intervals[True], intervals[False])

    print(f"Sum of last visited: {sum_last_visited}")


def resolve_jump(previous, jump, visited, arcs, max_position):
    """Return where this jump lands, or None if no landing is possible."""
    # Try backwards first.
    target = previous - jump
    if (
        target >= 0
        and target not in visited
        and not crosses_any(sorted((previous, target)), arcs)
    ):
        return target

    # Fall back to forwards, sliding past any blocked spot.
    target = previous + jump
    while target in visited or crosses_any(sorted((previous, target)), arcs):
        target += 1
        if target - max_position > 1:
            return None
    return target


def crosses(a: List[int], b: List[int]) -> bool:
    # Disjoint (touching at an endpoint doesn't count as overlap).
    if a[1] < b[0] or b[1] < a[0]:
        return False

    # One fully inside the other.
    if (a[0] < b[0] and b[1] < a[1]) or (b[0] < a[0] and a[1] < b[1]):
        return False

    return True


def crosses_any(line: List[int], intervals: List[List[int]]):
    if len(intervals) == 0:
        return False
    for interval in intervals:
        if crosses(line, interval):
            return True

    return False


def plot_arcs(below_arcs: List[Tuple[int, int]], above_arcs: List[Tuple[int, int]]):
    """Draw the below/above arcs as half-circles hanging off a shared horizontal line."""
    _, ax = plt.subplots(figsize=(12, 6))
    ax.axhline(0, color="black", linewidth=1, zorder=1)

    for a, b in below_arcs:
        _plot_arc(ax, a, b, below=True, color="tab:blue")
    for a, b in above_arcs:
        _plot_arc(ax, a, b, below=False, color="tab:red")

    ax.grid(False)
    ax.set_aspect("equal")
    ax.set_yticks([])
    plt.show()


def _plot_arc(ax, a: int, b: int, below: bool, color: str):
    center = (a + b) / 2
    radius = abs(b - a) / 2
    theta = np.linspace(0, np.pi, 100)
    x = center + radius * np.cos(theta)
    y = radius * np.sin(theta)
    if below:
        y = -y
    ax.plot(x, y, color=color, linewidth=1.5, zorder=2)


def parse_file(file_name: str) -> List[Tuple[int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    ornaments = []
    with open(abs_file_path, "r") as f:
        for line in f:
            ornaments.append(tuple(map(int, line.strip().split(","))))
    return ornaments


part1()
part2()
part3()
