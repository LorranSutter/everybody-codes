import os
import math
import bisect
from typing import Tuple

from utils.timer import timer

"""
Part 1:
- The key insight is that the next filled square is just the square of the ceiling of the square root.
  For 10 pine cones, ceil(√10) = 4, so the target is 4² = 16 and we need 16 - 10 = 6 more.
- If we already have a perfect square, the ceiling gives its own root and we need nothing.

Part 2:
- The trick here is realizing that frames only come in multiples of 4. A k x k frame is the full square minus the
  empty (k - 2) x (k - 2) middle:
      k² - (k - 2)² = 4k - 4
- Starting at 3 x 3, that gives 8, 12, 16, 20, ... or 8 + 4i, which is what the list of frames holds. We then look
  for the first frame that is not smaller than our pine cones. If we hit one exactly we skip it, otherwise
  bisect_right gives us the next one up (anything below 8 lands on the 3 x 3 frame).
- The binary search was overkill. Some similar math to the other parts would suffice
  (round up to the next multiple of 4, with a minimum of 8).

Part 3:
- Same as part 1, but the square must have an odd side s and we lose the center cell, so it holds s² - 1 pine cones.
  We want the smallest odd s with s² - 1 >= pine_cones, and then we collect s² - 1 - pine_cones.
- Start from the same ceiling of the square root as in part 1, then fix it up for the odd rule:
  - if it's even, the next odd side is just +1. The odd side below is too small since it is under the root
  - if it's odd and its square equals pine_cones, the square is full but we need room for the hole, so we jump to
    the next odd side, +2
  - any other odd side has s² > pine_cones, so s² - 1 is enough
- For example, 25 pine cones: ceil(√25) = 5 is odd but 5² = 25, so we go to 7 and 7² - 1 - 25 = 23.
"""


@timer
def part1():
    pine_cones = parse_file("input01.txt")

    needed_pine_cones = 0
    for pine_cone in pine_cones:
        square_root = math.ceil(math.sqrt(pine_cone))
        needed_pine_cones += square_root**2 - pine_cone

    print(f"Needed pine cones: {needed_pine_cones}")


@timer
def part2():
    pine_cones = parse_file("input02.txt")
    pine_cone_frames = [8 + 4 * i for i in range(2500)]

    needed_pine_cones = 0
    for pine_cone in pine_cones:
        if pine_cone in pine_cone_frames:
            continue
        target = bisect.bisect_right(pine_cone_frames, pine_cone)
        needed_pine_cones += pine_cone_frames[target] - pine_cone

    print(f"Needed pine cones: {needed_pine_cones}")


@timer
def part3():
    pine_cones = parse_file("input03.txt")

    needed_pine_cones = 0
    for pine_cone in pine_cones:
        square_root = math.ceil(math.sqrt(pine_cone))
        if square_root % 2 == 0:
            square_root += 1
        elif square_root**2 == pine_cone:
            square_root += 2

        needed_pine_cones += square_root**2 - pine_cone - 1

    print(f"Needed pine cones: {needed_pine_cones}")


def parse_file(file_name: str) -> Tuple[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    pine_cones = []
    with open(abs_file_path, "r") as f:
        pine_cones = tuple(map(int, f.read().strip().split(",")))
    return pine_cones


part1()
part2()
part3()
