import os

from utils.timer import timer
from utils.utils import print_matrix, tcolors

"""
Preprocessing:
- We wrap the map in a one-cell ring of "." (water). That way every neighbour lookup is safe without bounds checks,
  and the "outside the map is water" rule from part 2 comes for free.

Part 1:
- The key insight is that we never need to rescan the whole map. Land only grows outwards from the centre, so the only
  cells that can flip are the ones touching land we already know. We keep those in a frontier (`to_explore`).
- Start with the centre as "#" and its 8 neighbours as the frontier. Each round we check every frontier cell: if at
  least 5 of its neighbours are "#" or a dark "1", it becomes land. Cells that don't make it stay in the frontier,
  because a neighbour might turn into land later and tip them over.
- Every new land cell drags its own 8 neighbours into the frontier (we filter out the ones that are already land).
  We stop when a whole round adds nothing. The answer is the number of cells added, plus 1 for the centre.
- Each round is simultaneous: we collect all the new cells first and only then write them to the grid. The final
  land is the same either way, since land never shrinks, but it keeps the rounds easy to reason about.

Part 2:
- Same land as part 1, then we turn the shoreline into sand "=" and grow it inwards with the very same `explore()`.
  The only difference is the roles: the cells that can flip are now "#" and the ones that count are "=".
- A land cell is shoreline if any of its 8 neighbours isn't "#". Thanks to the padding ring, cells on the edge of the
  map see water on their own, so no special case is needed.
- The frontier starts as the land cells touching the new sand, and then it grows the same way as before: a land cell
  becomes sand once at least 5 neighbours are sand.
- The answer is the shoreline cells plus whatever the growth added.

Part 3:
- The stamp is just `is_new_cell()` with a different neighbourhood: `DIRS_20` is the 5x5 square minus its four
  corners and minus the centre, which is 20 cells. Asking for `min_adj=20` means "all 20 must be land or tree".
- We sweep the map top to bottom, left to right, and plant a tree in place right away. This is on purpose: a tree
  planted earlier in the sweep can make a later stamp position valid, exactly as the statement describes.
- Then two growth rounds, each simultaneous (collect first, apply after) so a tree added in a round only helps in the
  next one. A land cell becomes a tree with at least 4 tree neighbours.
"""


DIRS_8 = [(-1, -1), (1, 1), (-1, 1), (1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
DIRS_20 = DIRS_8 + [
    (-2, -1),
    (-2, 0),
    (-2, 1),
    (2, -1),
    (2, 0),
    (2, 1),
    (-1, -2),
    (0, -2),
    (1, -2),
    (-1, 2),
    (0, 2),
    (1, 2),
]


def is_new_cell(
    grid: list[list[str]],
    r: int,
    c: int,
    adjacent: list[str],
    dirs: list[tuple[int]] = DIRS_8,
    min_adj: int = 5,
) -> bool:
    neighbors = 0
    for dr, dc in dirs:
        if grid[r + dr][c + dc] not in adjacent:
            continue

        neighbors += 1
        if neighbors >= min_adj:
            return True

    return False


def explore(
    grid: list[list[str]],
    to_explore: list[tuple[int]],
    cell_types: list[str],
    adjacent: list[str],
    new_cell_type: str,
) -> int:
    cell_count = 0
    is_more_to_explore = True
    while is_more_to_explore:
        is_more_to_explore = False

        new_to_explore = set()
        new_cells = set()
        for r, c in to_explore:
            if is_new_cell(grid, r, c, adjacent):
                new_cells.add((r, c))
            else:
                # Still border to explore
                new_to_explore.add((r, c))

        cell_count += len(new_cells)
        if len(new_cells) > 0:
            is_more_to_explore = True

            # Add new cell's borders to explore
            for r, c in new_cells:
                grid[r][c] = new_cell_type
                for dr, dc in DIRS_8:
                    new_to_explore.add((r + dr, c + dc))

            # Remove previously added cell
            new_to_explore = set(
                (r, c) for r, c in new_to_explore if grid[r][c] in cell_types
            )

        to_explore = list(new_to_explore)

    return cell_count


def build_land(grid: list[list[str]]) -> int:
    m, n = len(grid), len(grid[0])
    grid[m // 2][n // 2] = "#"

    # Initial surroundings
    to_explore = []
    for dr, dc in DIRS_8:
        to_explore.append((m // 2 + dr, n // 2 + dc))

    return explore(grid, to_explore, ["0", "1"], ["#", "1"], "#") + 1


def build_sand(grid: list[list[str]]) -> int:
    m, n = len(grid), len(grid[0])

    # Find sand adjacent to water
    new_sand = set()
    for r in range(1, m - 1):
        for c in range(1, n - 1):
            if grid[r][c] != "#":
                continue
            for dr, dc in DIRS_8:
                if grid[r + dr][c + dc] != "#":
                    new_sand.add((r, c))
                    break

    # Turn found sand into "="
    sand_count = 0
    to_explore = set()
    for r, c in new_sand:
        grid[r][c] = "="
        sand_count += 1

        # Save sand adjacents
        for dr, dc in DIRS_8:
            if grid[r + dr][c + dc] == "#":
                to_explore.add((r + dr, c + dc))

    # Filter only by land
    to_explore = set((r, c) for r, c in to_explore if grid[r][c] == "#")

    return sand_count + explore(grid, to_explore, ["#"], ["="], "=")


def build_tree(grid: list[list[str]]) -> int:
    m, n = len(grid), len(grid[0])

    tree_count = 0

    # Find stamp trees
    for r in range(1, m - 1):
        for c in range(1, n - 1):
            if grid[r][c] != "#":
                continue

            if is_new_cell(grid, r, c, ["#", "@"], DIRS_20, 20):
                grid[r][c] = "@"
                tree_count += 1

    # Grow phase
    for _ in range(2):
        new_trees = set()
        for r in range(1, m - 1):
            for c in range(1, n - 1):
                if grid[r][c] != "#":
                    continue

                if is_new_cell(grid, r, c, ["@"], DIRS_8, 4):
                    new_trees.add((r, c))

        for r, c in new_trees:
            grid[r][c] = "@"
            tree_count += 1

    return tree_count


def print_color_matrix(grid: list[list[str]]):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            match grid[r][c]:
                case "#":
                    grid[r][c] = f"{tcolors.GREEN}#{tcolors.RESET}"
                case "=":
                    grid[r][c] = f"{tcolors.YELLOW}={tcolors.RESET}"
                case "@":
                    grid[r][c] = f"{tcolors.VIOLET}@{tcolors.RESET}"
                case _:
                    grid[r][c] = f"{tcolors.BLUE}.{tcolors.RESET}"
    print_matrix(grid)


@timer
def part1():
    grid = parse_file("input01.txt")

    land_count = build_land(grid)

    print_color_matrix(grid)

    print(f"Number of land cells: {land_count}")


@timer
def part2():
    grid = parse_file("input02.txt")

    build_land(grid)
    sand_count = build_sand(grid)

    print_color_matrix(grid)

    print(f"Number of sand cells: {sand_count}")


@timer
def part3():
    grid = parse_file("input03.txt")

    build_land(grid)
    build_sand(grid)
    tree_count = build_tree(grid)

    print_color_matrix(grid)

    print(f"Number of tree cells: {tree_count}")


def parse_file(file_name: str) -> list[list[str]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    grid = []
    with open(abs_file_path, "r") as f:
        for line in f:
            grid.append(["."] + [cell for cell in line.strip()] + ["."])

    grid.insert(0, len(grid[0]) * ["."])
    grid.append(len(grid[0]) * ["."])
    return grid


part1()
part2()
part3()
