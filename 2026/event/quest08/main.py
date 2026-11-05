import os
from itertools import cycle

from utils.timer import timer
from utils.utils import tcolors

"""
Preprocessing:
- We keep the map exactly as it comes, dots included: digits become ints and dots stay as `"."`. The trick is that
  the dots turn the hex field into a plain rectangle, where each of the six hex directions is just a fixed step.
  Around an Ent `X` at `(r, c)`:

      . ↖ . ↗ .        ↖ (r-1, c-1)    ↗ (r-1, c+1)
      ← . X . →        ← (r,   c-2)    → (r,   c+2)
      . ↙ . ↘ .        ↙ (r+1, c-1)    ↘ (r+1, c+1)

- Diagonal moves land on an Ent every time, except in the dot padding outside the hexagon. For ← and → we move one
  column at a time instead of two. Either way, a dot just means "nothing here, keep walking": we skip it without
  touching the shadow, so the shadow still drops exactly one level per hex.

Part 1:
- The key insight is that shadows only travel along the energy direction, so the field splits into independent
  lines parallel to ↘. Each line is a plain 1D scan: walk it from the edge the energy comes from, and count the Ents
  that stick out above the shadow reaching them.
- `calculate_energy()` fires one of these rays from every cell on the entry edges. For ↘ that's every column of the
  top row plus every row of the left column, starting from row 1 so the corner isn't fired twice. Together these
  rays cover every cell of the grid exactly once.
- Along a ray we carry `height`, the shadow reaching the current hex. If the Ent is taller, it gets energy and its
  height becomes the new shadow. Either way the shadow drops by one before moving on.
- There is an advantage here: the "shaded Ents still cast their own shadow" rule comes for free. A shaded Ent is no
  taller than the shadow on top of it, so its own shadow can never beat the one we're already carrying.

Part 2:
- Same scan as part 1, run once per direction and summed. The only real work is picking the entry edges for each
  direction, which is what the `params` list spells out.
- Diagonals enter through a row and a column (minus the shared corner, so it's not fired twice), like ↘ did in
  part 1. ← and → only need one column, since every row is its own ray.

Part 3:
- Same six-direction scan as part 2, but the circuit now runs nonstop with `cycle(params)` and the field changes as
  we go. Each inner list of `params` is one round, since a diagonal round needs both of its entry edges.
- One tricky thing is that all shadows must be determined before any Ent grows, while we grow Ents in place mid-ray.
  That's still fine: each cell sits on exactly one ray per round, and the ray reads `height = grid[r][c]` before
  bumping it, so no one ever sees a grown Ent until the next round.
- Seeds live in the grid as heights ≤ 0. When a 9 receives energy it goes to 10, we count a warrior and drop it to
  -2. Every cell is visited once per round, so a seed ticks up by one each round until it sprouts:

      round k      9 gets energy  →  -2   warrior leaves
      round k+1   -2              →  -1   underground
      round k+2   -1              →   0   underground
      round k+3    0              →   1   underground (ticks after the check, so no energy)
      round k+4    1                      sprouted, a normal Ent again

- The other tricky thing is that the shadow is now clamped at 0 (`if height > 0`). In parts 1 and 2 a negative
  shadow was harmless since every Ent is at least 1, but now a seed at 0 would happily beat a shadow of -1 and soak
  up energy. Seeds also cast no shadow: they never set `height`, so the incoming shadow keeps fading right over them.
- We check the army size after each full round, so the round that crosses 100000 is still counted. This is a plain
  simulation, a little bit brute force, but it only takes about 6k rounds on the real input.
- Obs: `print_field()` draws the field after the last round, with the Ents that received energy in yellow and seeds
  as a red `X`. Handy for eyeballing the simulation.
"""


def calculate_energy(
    grid: list[list[str | int]],
    start_row: int,
    start_col: int,
    increment_row: int,
    increment_col: int,
    min_range: int,
    max_range: int,
) -> int:
    if start_row >= 0 and start_col >= 0:
        raise Exception("Only one start can be >= 0")

    m, n = len(grid), len(grid[0])
    total_energy = 0

    for i in range(min_range, max_range):
        if start_row >= 0:
            r, c = start_row, i
        else:
            r, c = i, start_col

        height = 0
        while r < m and c < n and r >= 0 and c >= 0:
            if grid[r][c] == ".":
                r += increment_row
                c += increment_col
                continue

            if grid[r][c] > height:
                total_energy += 1
                height = grid[r][c]

            height -= 1
            r += increment_row
            c += increment_col

    return total_energy


def calculate_energy_with_growth(
    grid: list[str],
    start_row: int,
    start_col: int,
    increment_row: int,
    increment_col: int,
    min_range: int,
    max_range: int,
) -> tuple[int, int, set[tuple[int]]]:
    if start_row >= 0 and start_col >= 0:
        raise Exception("Only one start can be >= 0")

    m, n = len(grid), len(grid[0])
    total_energy, warriors = 0, 0
    energized = set()

    for i in range(min_range, max_range):
        if start_row >= 0:
            r, c = start_row, i
        else:
            r, c = i, start_col

        height = 0
        while r < m and c < n and r >= 0 and c >= 0:
            if grid[r][c] == ".":
                r += increment_row
                c += increment_col
                continue

            if grid[r][c] > height:
                total_energy += 1
                height = grid[r][c]
                grid[r][c] += 1
                energized.add((r, c))

                if grid[r][c] > 9:
                    warriors += 1
                    grid[r][c] = -2

            elif grid[r][c] < 1:
                grid[r][c] += 1

            if height > 0:
                height -= 1

            r += increment_row
            c += increment_col

    return total_energy, warriors, energized


def print_field(grid: list[list[str | int]], sep: str, energized: set[tuple[int]]):
    min_width = 0
    for r in range(len(grid)):
        row = []
        for c in range(len(grid[r])):
            item = grid[r][c]
            if isinstance(item, int) and item < 1:
                item = f"{tcolors.RED}X{tcolors.RESET}"
            elif item == ".":
                item = " "
            if (r, c) in energized:
                row.append(f"{tcolors.YELLOW}{str(item)}{tcolors.RESET}")
            else:
                row.append(f"{tcolors.BLACK}{str(item)}{tcolors.RESET}")

        print(sep.join(str(elem).rjust(min_width) for elem in row))


@timer
def part1():
    grid = parse_file("input01.txt")
    m, n = len(grid), len(grid[0])

    total_energy = 0

    # NE ↘ 0, [0, n]
    total_energy += calculate_energy(grid, 0, -1, 1, 1, 0, n)
    # NE ↘ [1, m], 0
    total_energy += calculate_energy(grid, -1, 0, 1, 1, 1, m)

    print(f"Total units of energy: {total_energy}")


@timer
def part2():
    grid = parse_file("input02.txt")
    m, n = len(grid), len(grid[0])

    params = [
        # NE ↘ 0, [0, n]
        [0, -1, 1, 1, 0, n],
        # NE ↘ [1, m], 0
        [-1, 0, 1, 1, 1, m],
        # NW ↙ 0, [0, n]
        [0, -1, 1, -1, 0, n],
        # NW ↙ [1, m], n
        [-1, n - 1, 1, -1, 1, m],
        # W ← [0, m], n
        [-1, n - 1, 0, -1, 0, m],
        # SW ↖ m, [0, n]
        [m - 1, -1, -1, -1, 0, n],
        # SW ↖ [0, m - 1], n
        [-1, n - 1, -1, -1, 0, m - 1],
        # SE ↗ m, [0, n]
        [m - 1, -1, -1, 1, 0, n],
        # SE ↗ [0, m - 1], 0
        [-1, 0, -1, 1, 0, m - 1],
        # E → [0, m], 0
        [-1, 0, 0, 1, 0, m],
    ]

    total_energy = sum(calculate_energy(grid, *p) for p in params)

    print(f"Total units of energy: {total_energy}")


@timer
def part3():
    grid = parse_file("input03.txt")
    m, n = len(grid), len(grid[0])
    army_size = 100000

    params = [
        # NE group
        [
            # ↘ 0, [0, n]
            [0, -1, 1, 1, 0, n],
            # ↘ [1, m], 0
            [-1, 0, 1, 1, 1, m],
        ],
        # NW group
        [
            # ↙ 0, [0, n]
            [0, -1, 1, -1, 0, n],
            # ↙ [1, m], n
            [-1, n - 1, 1, -1, 1, m],
        ],
        # W group
        [
            # ← [0, m], n
            [-1, n - 1, 0, -1, 0, m],
        ],
        # SW group
        [
            # ↖ m, [0, n]
            [m - 1, -1, -1, -1, 0, n],
            # ↖ [0, m - 1], n
            [-1, n - 1, -1, -1, 0, m - 1],
        ],
        # SE group
        [
            # ↗ m, [0, n]
            [m - 1, -1, -1, 1, 0, n],
            # ↗ [0, m - 1], 0
            [-1, 0, -1, 1, 0, m - 1],
        ],
        # E group
        [
            # → [0, m], 0
            [-1, 0, 0, 1, 0, m],
        ],
    ]

    total_energy, total_warriors, rounds = 0, 0, 0
    energized = set()
    for param in cycle(params):
        for p in param:
            energy, warriors, energized = calculate_energy_with_growth(grid, *p)
            total_energy += energy
            total_warriors += warriors
        rounds += 1

        if total_warriors >= army_size:
            break

    print()
    print_field(grid, "", energized)
    print()

    print(f"Total rounds: {rounds}")
    print(f"Total warriors: {total_warriors}")
    print(f"Total units of energy: {total_energy}")


def parse_file(file_name: str) -> list[list[str | int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    grid = []
    with open(abs_file_path, "r") as f:
        for line in f:
            new_line = []
            for item in line.strip():
                if item != ".":
                    item = int(item)
                new_line.append(item)
            grid.append(new_line)
    return grid


part1()
part2()
part3()
