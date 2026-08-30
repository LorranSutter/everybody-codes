import os
from typing import List
from itertools import cycle
from collections import Counter

from utils.timer import timer

"""
Preprocessing:
- The problem gives the input as columns of dancers standing one behind another, but it's easier to
  work with rows. So we read the file into a matrix and transpose it, turning each column of dancers
  into a row. That makes adding and removing dancers from a column a plain list operation.
- We also wrap the matrix in a Dancers class that keeps its size (the number of columns) handy and
  bundles the helpers we need: dance() to move a clapper, dancers_hash() to fingerprint the current
  arrangement, and shout() to form the end-of-round number by concatenating the first dancer of each
  row.

Part 1:
- This is a plain simulation: run the rounds one at a time and read off the final shout. Every bit of
  the puzzle's "dance around the column high-fiving hands until the count matches your chest number"
  rule is folded into a single list insertion inside Dancers.dance() (see its docstring for the index
  arithmetic).
- Here we cycle the clapper column as 0, 1, 2, 3, 0, 1, ... for 10 rounds and print the last shout().

Part 2:
- The first instinct was to look for a cycle: the first time a shout repeats, treat that as the start
  of a loop and jump straight to the 2024th repeat with some arithmetic. That works on sample 2 but
  not in general - the same shout can come up while the grid underneath is in a completely different
  configuration, so an early repeated shout doesn't actually prove we've found a cycle.
- So we settle for brute force: keep dancing round after round, tally every shout in a Counter, and
  stop the moment one shout's count reaches 2024. The answer is that shout times the round we stopped
  on.

Part 3:
- The cycle idea from part 2 finally pays off, this time keyed on the whole arrangement. After each
  round we hash the entire dancer configuration (dancers_hash()) into a set, and the first time we
  land on one we've seen before, the dance is doomed to replay forever - so the highest shout so far
  is the highest that can ever happen.
- This is safe even though we don't store which column claps next alongside the hash. Every round
  moves one dancer from column c to column c+1, so across a group of four rounds the column lengths go
  [s-1,s+1,s,s] -> [s-1,s,s+1,s] -> [s-1,s,s,s+1] -> [s,s,s,s], a different shape at each phase. The
  lengths are part of the configuration, so two matching configs sit at the same point in the
  0,1,2,3 cycle and a repeat really is a repeat.
- We keep the largest shout seen along the way and print it once that repeat shows up.
"""


class Dancers:
    def __init__(self, dancers: List[List[int]]):
        self.dancers = dancers
        self.size = len(dancers)

    def dance(self, col: int):
        """
        Move one clapper around the column to their right and absorb them into it.

        - The clapper is the first dancer of column `col`; we pop them off and pick target_col, the
          column to the right, wrapping column 4 -> column 1 with `(col + 1) % size`.
        - Let `idx` be the clapper's chest number and `n = len(target_col)` once the clapper has left
          their own column. The clapper high-fives hands while the crowd counts: 1..n down the left
          side, n+1..2n back up the right side, then the same again. Absorption happens on the clap
          whose count equals `idx`, so we only need `idx` within one lap of 2n hands:
              position = (idx - 1) % (2 * n)      # the -1 turns the 1-based count into an index
        - position < n: the clapper is on the left side, high-fiving the dancer at index `position`,
          and is absorbed *in front of* them -> target_col.insert(position, idx).
        - position >= n: the clapper is on the right side coming back up. Count n+1 is the bottom
          dancer and count 2n is the top one, so the high-fived dancer sits at index `2n - position - 1`
          and the clapper is absorbed *behind* them, at index `2n - position` - which is what
          `position = 2 * len(target_col) - position` rewrites it to before the same insert call.

        Worked examples, inserting into a column of n = 4:
          idx = 2 -> position = (2 - 1) % 8 = 1, left side,  insert at 1 (clapper becomes the 2nd dancer)
          idx = 5 -> position = (5 - 1) % 8 = 4, right side, 8 - 4 = 4, insert at 4 (behind the last dancer)
        """
        idx = self.dancers[col][0]
        self.dancers[col].pop(0)
        target_col = self.dancers[(col + 1) % self.size]
        position = (idx - 1) % (2 * len(target_col))
        if position >= len(target_col):
            position = 2 * len(target_col) - position
        target_col.insert(position, idx)

    def dancers_hash(self) -> int:
        return hash(tuple(tuple(row) for row in self.dancers))

    def shout(self) -> int:
        return int("".join(str(self.dancers[i][0]) for i in range(self.size)))


@timer
def part1():
    dancers = parse_file("input01.txt")
    dancers = Dancers(dancers)

    rounds = 10
    for i in cycle(range(dancers.size)):
        if rounds <= 0:
            break

        dancers.dance(i)
        rounds -= 1

    shouted = dancers.shout()
    print(f"Number shouted: {shouted}")


@timer
def part2():
    dancers = parse_file("input02.txt")
    dancers = Dancers(dancers)

    rounds = 0
    target_repeats = 2024
    shouts_count = Counter()
    for i in cycle(range(dancers.size)):
        dancers.dance(i)

        shouted = dancers.shout()
        shouts_count[shouted] += 1
        rounds += 1
        if shouts_count[shouted] == target_repeats:
            break

    result = rounds * shouted
    print(f"Result after {target_repeats} repeats: {result}")


@timer
def part3():
    dancers = parse_file("input03.txt")
    dancers = Dancers(dancers)

    seen_dancers = set()
    highest_shout = 0
    for i in cycle(range(dancers.size)):
        dancers.dance(i)
        dancers_config = dancers.dancers_hash()

        if dancers_config in seen_dancers:
            break
        seen_dancers.add(dancers_config)

        shouted = dancers.shout()
        if shouted > highest_shout:
            highest_shout = shouted

    print(f"Highest shout: {highest_shout}")


def parse_file(file_name: str) -> List[List[int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    dancers = []
    with open(abs_file_path, "r") as f:
        data = []
        for line in f:
            data.append(list(map(int, line.split(" "))))

        # Transpose dancers matrix
        dancers = [list(row) for row in zip(*data)]

    return dancers


part1()
part2()
part3()
