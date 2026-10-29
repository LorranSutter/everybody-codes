import os
import re
from dataclasses import dataclass
from itertools import cycle

from utils.timer import timer

"""
Preprocessing:
- Each line looks like `ISO-3210 7654` (or `ISO2-...` in part 3), so a regex splits it into the standard name, the
  weight pattern (the digits after the dash) and the vote itself. We keep the last two as strings since we need to
  walk them digit by digit.

Part 1:
- The key insight is that the "standard" is just a list of bases, one per digit. The digit at position i (counting
  from the right, starting at 0) is worth digit * base_i ** i. Every base is different, so it's not a regular number
  system, but the formula is the same one we use for decimal. Sum all the votes and we're done.

Part 2:
- Same as part 1, but the weight pattern may be shorter than the vote. The pattern repeats from right to left, so we
  reverse the weight and wrap it in `itertools.cycle`. Then `next()` hands us the base for each position starting at
  the rightmost digit, no matter how long the vote is.
- This also covers part 1, since a pattern with the exact length never wraps around.

Part 3:
- The key insight is that a vote is valid when no smaller number has the same value. The description tells us that
  different digit strings can land on the same value, e.g. `ISO-5322 1028` and `ISO-5322 1036` are both 137. That
  happens because the weights of lower positions can pay for a unit of a higher one: here the digit at position 1
  is worth 2, so lowering it by one and raising the units digit by 2 changes nothing.
- This means that we can't just look at one position. Any digit can be traded for a bunch of lower digits.
- Note: the current solution is brute force and not optimal. For each vote we convert every smaller number and check
  if one of them has the same score. The votes are small enough for this to finish in a fraction of a second, but
  it grows with the value of the vote.
- Faster solution (not implemented): build the smallest representation of the score directly, going from the most
  significant position down. At each position we pick the smallest digit (0-9) such that the remaining value can
  still be paid by the lower positions. That "can still be paid" check is a small memoized recursion that stops
  early when the remainder is negative or larger than 9 * the sum of the lower weights. The vote is valid only if
  this smallest representation is the vote itself. For `ISO2-3 23` (value 9) the top digit can be 0, since a
  single 9 in the units covers everything, so we get `09` and `23` is discarded.
"""


@dataclass(frozen=True)
class Vote:
    standard: str
    weight: str
    vote: str


@timer
def part1():
    votes = parse_file("input01.txt")

    final_score = 0
    for vote in votes:
        final_score += convert_vote(vote.weight, vote.vote)

    print(f"Final score: {final_score}")


@timer
def part2():
    votes = parse_file("input02.txt")

    final_score = 0
    for vote in votes:
        final_score += convert_vote(vote.weight, vote.vote)

    print(f"Final score: {final_score}")


@timer
def part3():
    votes = parse_file("input03.txt")

    final_score = 0
    for vote in votes:
        score = convert_vote(vote.weight, vote.vote)
        for v in range(int(vote.vote) - 1, 0, -1):
            if convert_vote(vote.weight, str(v)) == score:
                break
        else:
            final_score += score

    print(f"Final score: {final_score}")


def convert_vote(weight: str, vote: str) -> int:
    score = 0
    n = len(vote)
    w = cycle(weight[::-1])
    for i in range(len(vote) - 1, -1, -1):
        score += int(vote[i]) * int(next(w)) ** (n - i - 1)

    return score


def parse_file(file_name: str) -> list[Vote]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    votes = []
    with open(abs_file_path, "r") as f:
        for line in f:
            standard, weight, vote = re.findall(r"(ISO2?)-(\d+)\s(\d+)", line.strip())[
                0
            ]
            votes.append(Vote(standard, weight, vote))
    return votes


part1()
part2()
part3()
