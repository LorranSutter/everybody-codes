import os
import math
import heapq
from typing import List, Tuple
from collections.abc import Callable

from utils.timer import timer
from utils.utils import print_matrix, tcolors

"""
Preprocessing:
- parse_file records the (row, col) of S and of @, then blanks both to 0 before parsing: closing the
  loop at S is free, and the volcano centre carries no cost. Everything else is a digit, so the grid
  ends up as a plain list of ints.
- Naming heads-up: the code calls the volcano (Xv, Yv), but X is the row index and Y is the column
  index. The distance test is symmetric so it doesn't matter for parts 1 and 2, but it's worth
  keeping straight when reading part 3.

Part 1:
- Walk every cell and keep it if it sits inside the lava circle of radius 10, using the puzzle's own
  test (Xv - x)**2 + (Yv - y)**2 <= R**2. Sum those cell values; blank the rest.
- That's the whole part, a direct double loop over the grid.

Part 2:
- Same circle test as part 1, but now we sweep the radius from 1 outward (up to half the grid, where
  the lava hits an edge) and want the single step that destroys the most.
- The trick is that we mutate the grid as we go: once a cell is counted at some radius we set it to
  '.', so each larger radius only ever sums the fresh ring it just reached, never cells an earlier
  step already burned. That gives us the per-step destruction directly.
- Track the largest ring sum and the radius it happened at; the answer is their product.

Part 3:
- Here things get interesting. Underneath it's a weighted shortest path (Dijkstra over the digit
  costs), but the hard part is forcing that path to be a closed loop that actually encircles the
  volcano.
- The key insight: cut the grid along the ray running straight down from the volcano. Every cell in
  the volcano's column with row > Xv is off limits (that's the `allowed` lambda). Then build the loop
  as two independent shortest paths out of S:
    * S  ->  left  = (Xv + r, Yv - 1)   (just left of the ray, r rows below the volcano)
    * S  ->  right = (Xv + r, Yv + 1)   (just right of the ray)
  and glue them through the one cell sitting between them, (Xv + r, Yv), whose cost we add by hand.
- Why that makes a loop around the volcano: neither half may touch the ray, so the closed curve
  S -> left -> (Xv+r, Yv) -> right -> S crosses that downward ray exactly once, at the glue cell. A
  closed curve that crosses the ray from the volcano an odd number of times has to enclose the
  volcano (ray casting). One crossing, so the volcano is trapped.

      row 0:  . . . S . . .      S      start, directly above the volcano
      row 1:  . . a . b . .      a / b  the two half-paths (S->left, S->right)
      row 2:  . a . @ . b .      @      volcano centre
      row 3:  . a . x . b .      x      forbidden ray (column Yv, rows below the volcano)
      row 4:  . . L g R . .      L / R  the (Xv+r, Yv-1) and (Xv+r, Yv+1) endpoints
      row 5:  . . . x . . .      g      glue cell (Xv+r, Yv), on the ray, paid for by hand

- The glue cell is forbidden to Dijkstra, but it's always on the final loop with no alternative, so
  leaving it out of the search costs nothing: we just add grid[Xv+r][Yv] to the total afterwards.
- Running the two searches independently also means cells the halves share near S get counted twice,
  which is exactly what the puzzle wants ("segments below S are used twice").
- Timing: the lava gains one radius unit every 30 seconds. We try r = 1, 2, 3, ... and for each r we
  first expand_lava to blank every cell within radius r-1 (the loop finishes after the lava reached
  r-1 but before it reaches r), then require the finished loop to cost strictly less than r * 30. The
  first r that clears that wins.
- The radius when the loop closes is r-1, not r: radius r-1 was already tried and failed, so its cost
  was >= (r-1) * 30, and the loop only grows with r, so the finish time lands in [(r-1)*30, r*30) and
  the lava is still at r-1. Hence the final result is dist_total * (r - 1).

Obs: two approaches that don't work here. Dropping the first half's cells into a visited set and
  banning them on the second pass (the puzzle explicitly allows reusing cells), and picking three or
  four fixed waypoints around the volcano instead of the single ray cut (nothing guarantees the
  shortest loop passes through all of them).
"""


@timer
def part1(plot: bool = False):
    grid, volcano, _ = parse_file("input01.txt")

    radius = 10
    radius_squared = radius * radius
    Xv, Yv = volcano

    sum_cells = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if (Xv - x) ** 2 + (Yv - y) ** 2 <= radius_squared:
                sum_cells += grid[x][y]
            else:
                grid[x][y] = "."

    if plot:
        print_matrix(grid)

    print(f"Sum of the cells destroyed: {sum_cells}")


@timer
def part2(plot: bool = False):
    grid, volcano, _ = parse_file("input02.txt")
    Xv, Yv = volcano

    max_sum = 0
    max_radius = 0
    for r in range(1, len(grid) // 2 + 1):
        radius_squared = r * r
        sum_cells = 0
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if (
                    grid[x][y] != "."
                    and (Xv - x) ** 2 + (Yv - y) ** 2 <= radius_squared
                ):
                    sum_cells += grid[x][y]
                    grid[x][y] = "."

        if sum_cells > max_sum:
            max_sum = sum_cells
            max_radius = r

    if plot:
        print_matrix(grid)

    print(f"Greatest destruction: {max_radius*max_sum}")


@timer
def part3(plot: bool = False):
    grid, volcano, start = parse_file("input03.txt")
    Xv, Yv = volcano
    volcano_cycle = 30

    allowed = lambda c: not (c[1] == Yv and c[0] > Xv)
    for r in range(1, len(grid)):
        expand_lava(grid, volcano, r - 1)
        path = []
        left = (Xv + r, Yv - 1)
        right = (Xv + r, Yv + 1)

        d1, p = dijkstra(grid, start, left, allowed)
        path.extend(p)
        if d1 == -1 or d1 > r * volcano_cycle:
            continue

        d2, p = dijkstra(grid, start, right, allowed)
        path.extend(p)
        if d2 == -1 or d2 > r * volcano_cycle:
            continue

        dist_total = d1 + d2 + grid[Xv + r][Yv]
        if dist_total < r * volcano_cycle:
            break

    if plot:
        print_grid(grid, path + [(Xv + r, Yv)])

    print(f"Recurlia loop: {dist_total*(r-1)}")


def expand_lava(grid: List[List[int]], volcano: Tuple[int, int], radius: int):
    if radius < 1:
        return

    radius_squared = radius * radius
    Xv, Yv = volcano
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if (Xv - x) ** 2 + (Yv - y) ** 2 <= radius_squared:
                grid[x][y] = "."


def dijkstra(
    grid: List[List[int]],
    start: Tuple[int, int],
    end: Tuple[int, int],
    condition: Callable[[Tuple[int, int]], bool],
) -> Tuple[int, List[Tuple[int]]]:
    m, n = len(grid), len(grid[0])
    # Priority queue
    pq = []
    dist = {}
    parent = {}
    for i in range(m):
        for j in range(n):
            dist[(i, j)] = math.inf
            parent[(i, j)] = None
    dist[start] = 0
    heapq.heappush(pq, (0, start))

    dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))

    while pq:
        d, u = heapq.heappop(pq)

        if u == end:
            # Reconstruct path
            path = []
            curr = end
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return d, path

        # If this distance not the latest shortest one, skip it
        if d > dist[u]:
            continue

        for dr, dc in dirs:
            v = (u[0] + dr, u[1] + dc)
            if not condition(v):
                continue
            if v[0] < 0 or v[0] >= m or v[1] < 0 or v[1] >= n:
                continue

            w = grid[v[0]][v[1]]
            if w == ".":
                continue

            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    return -1, []


def print_grid(grid: List[List[int]], path: List[Tuple[int, int]], sep: str = ""):
    if path:
        new_grid = [row[:] for row in grid]
        for p in path:
            new_grid[p[0]][
                p[1]
            ] = f"{tcolors.GREEN}{new_grid[p[0]][p[1]]}{tcolors.RESET}"
        print_matrix(new_grid, sep)
    else:
        print_matrix(grid, sep)


def parse_file(
    file_name: str,
) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    grid = []
    volcano = None
    start = None
    with open(abs_file_path, "r") as f:
        for i, line in enumerate(f):
            if "S" in line:
                start = (i, line.index("S"))
                line = line.replace("S", "0")
            if "@" in line:
                volcano = (i, line.index("@"))
                line = line.replace("@", "0")

            grid.append(list(map(int, (cell for cell in line.strip()))))
    return grid, volcano, start


part1()
part2()
part3()
