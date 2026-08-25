import os
from typing import List

from utils.timer import timer
from utils.utils import print_matrix

"""
Preprocessing:
- The grid is parsed into `-1` for non-diggable cells (both the original `.` squares and an extra ring of `-1`
  padding added around the whole grid) and `0` for diggable `#` cells. The padding ring means neighbor lookups
  never need bounds checks, and it also gives Part 3 its "infinite `.` surroundings" for free.

Part 1:
- The key insight is that digging one layer at a time, over and over, is the same as computing - for every
  diggable cell - its distance to the nearest non-diggable cell or grid edge, like eroding the map ring by ring
  the way you'd peel an onion. A cell's height can only go from h to h+1 once every neighbor already sits at
  height h or above (treating non-diggable neighbors as a fixed floor of 0), which is exactly the rule that the
  slope must never differ by more than one.
- `dig()` implements one erosion pass: for each interior cell that's still diggable (`current >= 0`), it checks
  its four side-to-side/top-to-bottom neighbors. If any neighbor's height (floored at 0 for non-diggable cells)
  is lower than the current cell's height, the cell can't be raised yet, so the `for...else` loop breaks and
  skips it. Otherwise every neighbor already supports the next layer, so the cell is queued in `digs`. Queued
  cells are only bumped by 1 after the whole grid has been scanned, so a pass never mixes in this round's
  already-updated heights.
- `part1()` just calls `dig()` in a loop, adding up how many cells got dug each pass, until a pass digs
  nothing. The running total is the number of blocks removed, which, by the insight above, ends up being the
  sum of every cell's final "distance to the nearest wall" value.
- Here's a small example showing why the floor-at-0 trick matters:
    ..#..
    .###.
    ..#..
  becomes, after parsing, a grid where `.` is `-1` and `#` is `0`. 
    -1 -1  0 -1 -1
    -1  0  0  0 -1
    -1 -1  0 -1 -1

  On the first `dig()` pass every `#` cell has all four neighbors at `max(-1, 0) = 0`, 
  which is not less than its own current height of `0`, so every `#` cell gets dug once.
    -1 -1  1 -1 -1
    -1  1  1  1 -1
    -1 -1  1 -1 -1
  
  On the second pass, only the centre cell has all four neighbors already raised to height
  1 (the four arm cells still touch a `.` neighbor, which floors to `max(-1, 0) = 0 < 1`), so only the centre
  cell is dug again - matching the diamond shape you'd expect from an erosion process that gets shallower
  toward its points.
    -1 -1  1 -1 -1
    -1  1  2  1 -1
    -1 -1  1 -1 -1

Part 2:
- Same algorithm as Part 1, run against the larger map - no code changes, just a bigger grid to erode.

Part 3:
- Same erosion idea as Part 1, but `dig(grid, diagonals=True)` swaps the four side-to-side/top-to-bottom
  offsets for the eight king-move offsets, so a cell also can't rise above its diagonal neighbors by more than
  one. The "distance to the nearest wall" that Part 1 computes implicitly is now measured in king moves
  (Chebyshev distance) instead of the diamond-shaped distance from Parts 1-2.
- The puzzle frames "several separate areas" and being "surrounded by `.` infinitely" as new complications, but
  the code doesn't need to treat either specially: `dig()` only ever looks at a cell's immediate neighbors, so
  disconnected `#` regions erode independently just by construction, and the `-1` padding ring added in
  `parse_file()` already behaves like the infinite `.` border.
"""


@timer
def part1():
    grid = parse_file("input01.txt")

    total_digs = 0
    new_digs = 1
    while new_digs > 0:
        new_digs = dig(grid)
        total_digs += new_digs

    print(f"Earth blocks removed: {total_digs}")


@timer
def part2():
    grid = parse_file("input02.txt")

    total_digs = 0
    new_digs = 1
    while new_digs > 0:
        new_digs = dig(grid)
        total_digs += new_digs

    print(f"Earth blocks removed: {total_digs}")


@timer
def part3():
    grid = parse_file("input03.txt")

    total_digs = 0
    new_digs = 1
    while new_digs > 0:
        new_digs = dig(grid, diagonals=True)
        total_digs += new_digs

    print(f"Earth blocks removed: {total_digs}")


def dig(grid: List[List[int]], diagonals: bool = False):
    neighbors_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    neighbors = neighbors_8 if diagonals else neighbors_4

    digs = set()
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            current = grid[i][j]
            if current < 0:
                continue
            for di, dj in neighbors:
                if max(grid[i + di][j + dj], 0) < current:
                    break
            else:
                digs.add((i, j))

    for d in digs:
        grid[d[0]][d[1]] += 1

    return len(digs)


def parse_file(file_name: str) -> List[List[int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    grid = []
    with open(abs_file_path, "r") as f:
        for line in f:
            grid.append([-1] + [-1 if l == "." else 0 for l in line.strip()] + [-1])

    grid.insert(0, [-1] * len(grid[0]))
    grid.append([-1] * len(grid[0]))

    return grid


part1()
part2()
part3()
