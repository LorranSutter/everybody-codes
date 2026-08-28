import os
import sys
from typing import List, Tuple
from itertools import cycle
from enum import Enum

from utils.timer import timer
from utils.utils import tcolors

sys.setrecursionlimit(5000)

"""
Preprocessing:
- We model the whole floor as a big matrix, one entry per tile. Each entry is a Tile that just records whether there
  is a stitch on its `up`, `right`, `down` and `left` edge, plus which colour it ended up painted, and knows how to
  say whether it is isolated (a stitch on all four sides).
- This is a bit redundant: every shared edge between two tiles is stored twice, once from each side, so we carry
  roughly double the strictly necessary state. It keeps the isolation and flood-fill checks purely local, though.

Part 1:
- The whole challenge is building the grid correctly; once the stitches are in place, counting isolated tiles is
  just a scan. `build_grid` places the `up`/`down` stitches from the horizontal-offsets and the `left`/`right`
  stitches from the vertical-offsets.
- Each stitch line reads one digit from its offset sequence (cycled with `itertools.cycle` when it runs short) and
  then stitches every second tile. The digit is just a starting index into `range(start, size, 2)`:

    offset 0  ->  columns 0, 2, 4, 6, ...
    offset 1  ->  columns 1, 3, 5, 7, ...

- One thing to be mindful of: the main loops only walk rows `0..height-1` and columns `0..width-1`, setting the
  `up` edge of each tile (and the `down` edge of the tile above it). That never fills the `down` edge of the bottom
  row or the `right` edge of the last column, so those two borders are written in a separate small loop, pulling the
  next digit from the same cycled sequence so the pattern stays continuous.

Part 2:
- Same grid as part 1. The new idea: the regions carved out by the stitches always form a map that can be
  two-coloured, so no two neighbouring regions share a colour.
- We flood-fill one region at a time with a DFS that is allowed to step from a tile to a neighbour only when there
  is no stitch on the edge between them. Scanning tiles in row-major order, whenever we hit an uncoloured tile we
  start a fresh fill; its colour is chosen as the opposite of whichever already-coloured orthogonal neighbour we
  find first (that neighbour is necessarily in an adjacent region, since same-region tiles were already coloured by
  an earlier fill).
- Finally we scan every tile, tally isolated tiles per colour, and return the size of the larger group.

Obs: the recursive flood fill gets deep fast on large regions, which is why `sys.setrecursionlimit(5000)` is bumped
     up top.
     - Why it's deep: `dfs` recurses once per tile it colours, and each call stays on the stack until the whole
       region is filled. A long snaking region of a few thousand tiles means a few thousand stacked frames.
     - Why there's a ceiling: CPython runs recursion on the C call stack and enforces `sys.getrecursionlimit()`
       (1000 by default) to stop it from overflowing and segfaulting. `sys.setrecursionlimit(5000)` just raises
       that cap -- still a fixed number, and pushing it too high risks a real crash instead of a clean
       `RecursionError`.
     - The fix: write the flood fill as a `while stack:` loop with a plain list as the stack
       (`stack.append(neighbour)` / `node = stack.pop()`). The frontier now lives in a heap-allocated list, not in
       call frames, so the only limit is how much memory the list can grow to -- no recursion cap involved. (Same
       idea with a `collections.deque` and `popleft` if you'd rather do BFS.)

Part 3:
- The dense-grid + flood-fill approach from part 2 does not scale to this input. The floor is
  width x height = 31_415_926 x 577_215_664 ~= 1.8e16 tiles.
  Even at one byte per tile that is ~18 PB of memory; with an actual Tile object per cell (a `__slots__` instance is
  roughly a 56-byte header plus five 8-byte slots, ~96 bytes) it is ~1.7 EB. There is no way to materialise this
  grid, so part 3 needs a purely analytical count that never builds it.
- To be implemented
"""


class Color(Enum):
    COLOR_1 = 1
    COLOR_2 = 2


class Tile:
    __slots__ = ("up", "right", "down", "left", "color")

    def __init__(
        self,
        up: bool = False,
        right: bool = False,
        down: bool = False,
        left: bool = False,
        color: Color = None,
    ):
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.color = color

    def __repr__(self) -> str:
        return "".join(
            "1" if dir else "0" for dir in (self.up, self.right, self.down, self.left)
        )

    def is_isolated(self) -> bool:
        return all((self.up, self.right, self.down, self.left))


@timer
def part1():
    width, height, horizontal_shift, vertical_shift = parse_file("input01.txt")

    grid = build_grid(width, height, horizontal_shift, vertical_shift)
    isolated_count = count_isolated(grid)

    print(f"Isolated tiles: {isolated_count}")


@timer
def part2():
    width, height, horizontal_shift, vertical_shift = parse_file("input02.txt")

    grid = build_grid(width, height, horizontal_shift, vertical_shift)

    for i in range(height):
        for j in range(width):
            if grid[i][j].color is None:
                apply_color(grid, i, j)

    counts = {Color.COLOR_1: 0, Color.COLOR_2: 0}
    for i in range(height):
        for j in range(width):
            if grid[i][j].is_isolated():
                counts[grid[i][j].color] += 1

    print(f"Isolated tiles in the larger group: {max(counts.values())}")


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file("input_sample03.txt")
    pass


def build_grid(
    width: int, height: int, horizontal_shift: str, vertical_shift: str
) -> List[List[Tile]]:
    grid = [[Tile() for _ in range(width)] for _ in range(height)]
    h = cycle(horizontal_shift)
    v = cycle(vertical_shift)

    for i, bit in zip(range(height), h):
        for j in range(int(bit), width, 2):
            grid[i][j].up = True
            if i > 0:
                grid[i - 1][j].down = True

    # Manually write the down for the last line
    for j in range(int(next(h)), width, 2):
        grid[height - 1][j].down = True

    for j, bit in zip(range(width), v):
        for i in range(int(bit), height, 2):
            grid[i][j].left = True
            if j > 0:
                grid[i][j - 1].right = True

    # Manually write the rigth for the last column
    for i in range(int(next(v)), height, 2):
        grid[i][width - 1].right = True

    return grid


def count_isolated(grid: List[List[Tile]]) -> int:
    height = len(grid)
    width = len(grid[0])

    isolated_count = 0
    for i in range(height):
        for j in range(width):
            isolated_count += grid[i][j].is_isolated()

    return isolated_count


def apply_color(grid: List[List[Tile]], x: int, y: int) -> bool:
    height = len(grid)
    width = len(grid[0])
    painted = 0
    colors = {Color.COLOR_1: Color.COLOR_2, Color.COLOR_2: Color.COLOR_1}
    color = Color.COLOR_1

    if x > 0 and grid[x - 1][y].color is not None:
        color = colors[grid[x - 1][y].color]
    elif x < height - 1 and grid[x + 1][y].color is not None:
        color = colors[grid[x + 1][y].color]
    elif y > 0 and grid[x][y - 1].color is not None:
        color = colors[grid[x][y - 1].color]
    elif y < width - 1 and grid[x][y + 1].color is not None:
        color = colors[grid[x][y + 1].color]

    def dfs(_x: int, _y: int):
        nonlocal painted, color
        if grid[_x][_y].color is not None:
            return

        grid[_x][_y].color = color
        painted += 1

        if _x > 0 and not grid[_x][_y].up:
            dfs(_x - 1, _y)
        if _x < height - 1 and not grid[_x][_y].down:
            dfs(_x + 1, _y)
        if _y > 0 and not grid[_x][_y].left:
            dfs(_x, _y - 1)
        if _y < width - 1 and not grid[_x][_y].right:
            dfs(_x, _y + 1)

    dfs(x, y)
    return painted > 0


def print_grid(grid: List[List[Tile]], sep: str = "", min_width: int = 0):
    for row in grid:
        output = ""
        for elem in row:
            if elem.is_isolated():
                output += f"{tcolors.RED}{elem}{tcolors.RESET}".rjust(min_width) + sep
            elif elem.color == Color.COLOR_1:
                output += (
                    f"{tcolors.YELLOW}{elem}{tcolors.RESET}".rjust(min_width) + sep
                )
            elif elem.color == Color.COLOR_2:
                output += f"{tcolors.GREEN}{elem}{tcolors.RESET}".rjust(min_width) + sep
            else:
                output += f"{elem}".rjust(min_width) + sep
        print(output)


def parse_file(file_name: str) -> Tuple[int, int, str, str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    width, height = 0, 0
    horizontal_shift = 0
    vertical_shift = 0
    with open(abs_file_path, "r") as f:
        data = [d.split("=") for d in f.read().split("\n")]
        width = int(data[0][1])
        height = int(data[1][1])
        horizontal_shift = data[2][1]
        vertical_shift = data[3][1]
    return width, height, horizontal_shift, vertical_shift


part1()
part2()
# part3()
