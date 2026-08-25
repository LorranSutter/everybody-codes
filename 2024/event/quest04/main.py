import os
from typing import Tuple

from utils.timer import timer
from utils.utils import plot_points

"""
Part 1:
- All the nails just need to come down to the height of the shortest one, so the minimum height is
  the target, and the total strikes are the sum of how far each nail sticks out above it.

Part 2:
- Same as part 1, just a bigger set of nails: find the minimum height and sum the differences to it.

Part 3:
- Here nails can be driven down or pulled up, so we get to pick the target height instead of being
  stuck with the minimum. The number of strikes for a given target t is sum(|nail - t|) over all
  nails, and we want the t that minimizes that sum.
- The first instinct is to reach for the mean, since it's the "average" nail height. But the mean
  minimizes the sum of *squared* differences (sum((nail - t)^2)), not the sum of absolute differences
  we actually care about here. The value that minimizes sum(|nail - t|) is the median instead.
- Here's the intuition: pick any target t and look at how the total changes as we nudge t by one unit.
  Every nail below t has t - nail; nudging t up by 1 increases each of those terms by 1. Every nail
  above t has nail - t; nudging t up by 1 decreases each of those terms by 1. So the total strikes go
  down as long as there are more nails above t than below it, and go up once there are more below than
  above. The minimum sits right where the count above equals the count below — which is exactly the
  median, by definition.
- Worked example, nails 2, 4, 5, 6, 8 (sorted, so the median is already in the middle at 5): with
  t = 5, two nails (2 and 4) sit below and need 3 + 1 = 4 strikes up; two nails (6 and 8) sit above and
  need 1 + 3 = 4 strikes down. Total: 8 strikes, matching the puzzle's answer. Nudging t to 6 would
  add a strike for every nail still below it (three of them: 2, 4, 5) while only saving one strike on
  the nails above (8), making the total worse — confirming 5 is the balance point.
- Obs: the code sorts once and indexes the middle element (nails[len(nails) // 2]), which is the
  median for an odd-sized list. It happens not to matter here, but for an even-sized list this only
  grabs one of the two middle values — any point between them (including either one) gives the same
  minimal total, so it's still correct, just worth knowing why.
"""


@timer
def part1():
    nails = parse_file("input01.txt")

    min_height = min(nails)
    strikes = sum([nail - min_height for nail in nails])

    print(f"Minimum number of strikes: {strikes}")


@timer
def part2():
    nails = parse_file("input02.txt")

    min_height = min(nails)
    strikes = sum([nail - min_height for nail in nails])

    print(f"Minimum number of strikes: {strikes}")


@timer
def part3():
    nails = parse_file("input03.txt")

    nails = sorted(nails)
    median = nails[len(nails) // 2]

    strikes = sum([abs(nail - median) for nail in nails])
    print(f"Minimum number of strikes: {strikes}")


def parse_file(file_name: str) -> Tuple[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    nails = []
    with open(abs_file_path, "r") as f:
        nails = tuple(map(int, f.read().split("\n")))
    return nails


part1()
part2()
part3()
