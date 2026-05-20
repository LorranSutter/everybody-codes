import os
import math
import heapq
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from collections import deque, defaultdict
from dataclasses import dataclass
from shapely.geometry import LineString
from shapely.plotting import plot_line
from itertools import combinations

from utils.timer import timer
from utils.utils import tcolors

"""
Preprocessing:
- Read the input file and split into a list of strings representing the instructions.
- We created a class `Coordinate` to facilitate coordinate manipulation

Part 1:
- Ultimately, we want to apply a shortest path algorithm between the start and end points.
  So, we have a 3 step process here:
    1. Find corners and boundaries
        - Given the instructions, it is possible to simulate a walk through the tunnel and get the corners at each turn.
        - We also find the boundaries (x0, y0) and (x1, y1) where the tunnel is circumscribed
          This will be relevant for cases where the instructions leads to a place before the origin (0,0)
          (x0, y0)
                  -----------
                 |      ##   |
                 | ##   #    |
                 |  #   #    |
                 |  #####    |
                  -----------
                              (x1, y1)
    2. Build the tunnel and get new start and end positions
        - We want to construct the 2D grid representing the area where the tunnel is built.
        - This grid is pretty much empty spaces and has # where the tunnel is built.
        - Also, we build a barrier of # around the borders to limit the search space.
        - In case the instructions lead to a place before the origin, we need to adjust the boundaries.
          We calculate the shift_x and shift_y so the origin (0,0) is back to the top-left corner of the grid.
        - We also return the start and end positions ajusted by the shift_x and shift_y.
    3. Find shortest path
        - Having the grid with tunnel and boundaries done, we can perform a breadth-first search (BFS)
          to find the shortest path from start to end.

Part 2:
- Same as part 1, but with larger numbers.
- The algorithm from part 1 was efficient enough to handle larger inputs.

Part 3:
- Same as part 1 and 2, but with way bigger numbers, generating a grid of 77475258 X 86475248.
  Using BFS for this size in inpractable.
- In this case we wanted to model the problem in to a graph problem and apply another shortest path algorithm.
  In order to do that, have to find the compressed version of the original grid.
  This time we have a 5 step process:
    1. Find corners and expanded corners
      - Similarly to parts 1 and 2, we find the corners of the tunnel, but also the expanded corners.
      - In addition, we also want the expanded corners that are the points out of the existing corners:
              *
           *   #####
        ###    #
          #    #
          ######
         *      *
      - If we think intuitively, the shortest path will also include some expanded corner
    2. Build the walls
      - Similarly to part 1 and 2, we have to build the tunnel
      - Instead of representing the tunnel in the grid, we just calculate a list of segments
        that connects the corners. We will call it walls here.
    3. Build the graph edges
      - The graph we will work with will be all the possible paths among the expanded corners.
      - First we list all the combinations of pairs of expanded corners
      - Second, the only valid segments are the ones that don't intersect any walls
      - After filtering these, we get the list of valid graph edges
    4. Build the graph
      - We already have the edges that gives us an unweighted graph, but we need the distance between the corners
        and turn into a weighted graph.
      - Since we just have edges that do not intersect any walls, the distance between them will be the manhattan distance:
        distance = abs(A.x - B.x) + abs(A.y - B.y)
      - Now, we can build our adjacent matrix with coordinates and weights. E.g.:
        ( 0, 0) -> [(( 2, 1), 3)), ((3, 2), 5)), ((-2,-4), 6))]
        (-2,-8) -> [((-1,-8), 1)), ((4,-8), 6))]
    5. Find shortest path
      - Since we have a weighted graph, we can use Dijkstra's algorithm to find the shortest path
"""


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)


@timer
def part1():
    instructions = parse_file("input01.txt")

    corners, boundaries = find_corners_and_boundaries(
        instructions, Coordinate(0, 0), Coordinate(-1, 0)
    )
    tunnel, start, end = build_tunnel(corners, boundaries)
    path_length, path = find_shortest_path_with_trace(tunnel, start, end)

    for cell in path:
        tunnel[cell.x][cell.y] = tcolors.GREEN + "." + tcolors.RESET

    print_tunnel(tunnel)

    print(f"Shortest path length: {path_length-1}")


@timer
def part2():
    instructions = parse_file("input02.txt")

    corners, boundaries = find_corners_and_boundaries(
        instructions, Coordinate(0, 0), Coordinate(-1, 0)
    )
    tunnel, start, end = build_tunnel(corners, boundaries)
    path_length, path = find_shortest_path_with_trace(tunnel, start, end)

    for cell in path:
        tunnel[cell.x][cell.y] = tcolors.GREEN + "." + tcolors.RESET

    print_tunnel(tunnel)

    print(f"Shortest path length: {path_length-1}")


@timer
def part3():    
    instructions = parse_file("input03.txt")

    corners, expanded_corners = find_expanded_corners(
        instructions, Coordinate(0, 0), Coordinate(-1, 0)
    )

    # Build the walls of the tunnel
    walls = build_walls(corners)

    # Build all possible edges that connect the expanded corners
    expanded_corner_combs = list(combinations(expanded_corners, 2))
    all_edges = []
    for pair in expanded_corner_combs:
        all_edges.append(LineString([(pair[0].x, pair[0].y), (pair[1].x, pair[1].y)]))

    # Find the edges that do not intersect with any walls
    edges = [edge for edge in all_edges if not any(edge.intersects(walls))]

    graph = build_graph(edges)

    d, path = dijkstra(
        graph, (corners[0].x, corners[0].y), (corners[-1].x, corners[-1].y)
    )

    # path_line_string = [LineString([path[i], path[i + 1]]) for i in range(len(path) - 1)]
    # plot_tunnel(walls, edges, path_line_string)

    print(f"Shortest path: {path}")
    print(f"Shortest path length: {d}")


def find_expanded_corners(
    instructions: List[str], start: Coordinate, start_dir: Coordinate
) -> Tuple[List[Coordinate], List[Coordinate]]:
    """
    Calculate the expanded corners of the tunnel
    The expanded corners are the points out of the corners
          *
       *   #####
    ###    #
      #    #
      ######
     *      *
    """
    expanded_corner_map = {
        (Coordinate(-1, 0), Coordinate(0, 1)): Coordinate(-1, -1),
        (Coordinate(-1, 0), Coordinate(0, -1)): Coordinate(-1, 1),
        (Coordinate(1, 0), Coordinate(0, 1)): Coordinate(1, -1),
        (Coordinate(1, 0), Coordinate(0, -1)): Coordinate(1, 1),
        (Coordinate(0, -1), Coordinate(1, 0)): Coordinate(-1, -1),
        (Coordinate(0, 1), Coordinate(1, 0)): Coordinate(-1, 1),
        (Coordinate(0, -1), Coordinate(-1, 0)): Coordinate(1, -1),
        (Coordinate(0, 1), Coordinate(-1, 0)): Coordinate(1, 1),
    }
    pos = start
    dir = start_dir
    corners = []
    expanded_corners = []
    for instruction in instructions:
        side, length = instruction[0], int(instruction[1:])

        if side == "R":
            new_pos = Coordinate(pos.x + dir.y * length, pos.y - dir.x * length)
            new_dir = Coordinate(dir.y, -dir.x)
        else:
            new_pos = Coordinate(pos.x - dir.y * length, pos.y + dir.x * length)
            new_dir = Coordinate(-dir.y, dir.x)

        expanded_corner_dir = expanded_corner_map[(dir, new_dir)]
        expanded_corners.append(pos + expanded_corner_dir)
        corners.append(pos)

        dir = new_dir
        pos = new_pos

    # Add the final position to the list of corners
    corners.append(pos)

    # Replace first and last expanded corners by the start and end positions
    expanded_corners[0] = corners[0]
    expanded_corners[-1] = corners[-1]

    return corners, expanded_corners


def build_walls(corners: List[Coordinate]) -> List[LineString]:
    """
    Build the walls of the tunnel using the corner points
    """
    walls = []
    for i in range(1, len(corners) - 2):
        walls.append(
            LineString(
                [(corners[i].x, corners[i].y), (corners[i + 1].x, corners[i + 1].y)]
            )
        )

    # We remove the starting and ending walls to avoid detecting it as intersections

    # Remove the starting point from the first wall
    dir = get_direction(corners[0], corners[1])
    first_wall = LineString(
        [(corners[0].x + dir.x, corners[0].y + dir.y), (corners[1].x, corners[1].y)]
    )

    # Remove the ending point from the last wall
    dir = get_direction(corners[-2], corners[-1])
    last_wall = LineString(
        [(corners[-2].x, corners[-2].y), (corners[-1].x - dir.x, corners[-1].y - dir.y)]
    )

    walls.insert(0, first_wall)
    walls.append(last_wall)

    return walls


def build_tunnel(
    corners: List[Coordinate], boundaries: Tuple[Coordinate]
) -> Tuple[List[List[str]], Coordinate, Coordinate]:
    """
    Fill the 2D grid with # where the tunnel is present

    Returns:
        The filled grid
        The coordinates of the new corners
    """
    shift_x = abs(boundaries[0].x) if boundaries[0].x < 0 else 0
    shift_y = abs(boundaries[0].y) if boundaries[0].y < 0 else 0

    # Add 1 to include the starting point
    size_x = abs(boundaries[0].x) + abs(boundaries[1].x) + 1
    size_y = abs(boundaries[0].y) + abs(boundaries[1].y) + 1

    tunnel = [[" " for _ in range(size_y)] for _ in range(size_x)]

    # Fill the walls
    pos = corners[0]
    for corner in corners[1:]:
        dir = get_direction(pos, corner)
        if pos.x == corner.x:
            for i in range(pos.y + shift_y, corner.y + dir.y + shift_y, dir.y):
                tunnel[pos.x + shift_x][i] = "#"
        else:
            for i in range(pos.x + shift_x, corner.x + dir.x + shift_x, dir.x):
                tunnel[i][pos.y + shift_y] = "#"

        pos = corner

    # Add the boundaries
    tunnel.insert(0, ["#"] * size_y)
    tunnel.append(["#"] * size_y)
    for i in range(size_x + 2):
        tunnel[i].insert(0, "#")
        tunnel[i].append("#")

    new_corners = [
        Coordinate(pos.x + shift_x + 1, pos.y + shift_y + 1) for pos in corners
    ]
    start = Coordinate(corners[0].x + shift_x + 1, corners[0].y + shift_y + 1)
    end = Coordinate(corners[-1].x + shift_x + 1, corners[-1].y + shift_y + 1)

    tunnel[new_corners[0].x][new_corners[0].y] = " "
    tunnel[new_corners[-1].x][new_corners[-1].y] = " "

    return tunnel, start, end


def find_shortest_path_with_trace(
    tunnel: List[List[str]], start: Coordinate, end: Coordinate
) -> Tuple[int, List[Coordinate]]:
    """
    Performs a BFS from start to end in the tunnel and returns the shortest path length and coordinates

    Args:
        tunnel (List[List[str]]): A 2D list representing the tunnel grid
        start (Coordinate): The starting coordinate
        end (Coordinate): The ending coordinate

    Returns:
        shortest_path_length (int): The shortest path length
        shortest_path (List[Coordinate]): The coordinates of the shortest path
    """

    if not tunnel or tunnel[start.x][start.y] == "#" or tunnel[end.x][end.y] == "#":
        return -1, []  # Start or end is blocked

    queue = deque([start])

    # Store visited coordinates and their parent to trace back
    visited = {start: None}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        pos = queue.popleft()

        # If we've reached the destination, backtrack to find the path
        if pos == end:
            path = []
            curr = end
            while curr is not None:
                path.append(curr)
                curr = visited[curr]
            path.reverse()

            # Distance is the number of nodes in the path
            return len(path), path

        for dr, dc in directions:
            new_pos = Coordinate(pos.x + dr, pos.y + dc)

            if tunnel[new_pos.x][new_pos.y] == " " and new_pos not in visited:
                visited[new_pos] = pos
                queue.append(new_pos)

    return -1, []  # No path found


def find_corners_and_boundaries(
    instructions: List[str], start: Coordinate, start_dir: Coordinate
) -> Tuple[List[Coordinate], Tuple[Coordinate, Coordinate]]:
    """
    Walk through the tunnel and find the corners and boundaries

    Args:
        instructions List[str]): List of instructions in the format "R90" or "L90"
        start (Coordinate): Starting position of the tunnel
        start_dir (Coordinate): Starting direction (usually upwards)

    Returns:
        corners: List[Coordinate]
        boundaries: Tuple[Coordinate, Coordinate]
    """

    pos = start
    dir = start_dir
    boundaries = (Coordinate(0, 0), Coordinate(0, 0))
    corners = [pos]
    for instruction in instructions:
        side, length = instruction[0], int(instruction[1:])

        if side == "R":
            pos = Coordinate(pos.x + dir.y * length, pos.y - dir.x * length)
            dir = Coordinate(dir.y, -dir.x)
        else:
            pos = Coordinate(pos.x - dir.y * length, pos.y + dir.x * length)
            dir = Coordinate(-dir.y, dir.x)

        corners.append(pos)
        boundaries = (
            Coordinate(min(boundaries[0].x, pos.x), min(boundaries[0].y, pos.y)),
            Coordinate(max(boundaries[1].x, pos.x), max(boundaries[1].y, pos.y)),
        )

    return corners, boundaries


def build_graph(edges: List[LineString]) -> Dict[Tuple[int], List[Tuple[Tuple, int]]]:
    adj = defaultdict(list)

    for edge in edges:
        p1, p2 = tuple(edge.coords)
        p1, p2 = (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1]))

        # Manhattan distance
        dist = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

        adj[p1].append((p2, dist))
        adj[p2].append((p1, dist))

    return adj


def dijkstra(
    graph: Dict[Tuple[int], List[Tuple[Tuple, int]]], start: Tuple[int], end: Tuple[int]
) -> Tuple[int, List[Tuple[int]]]:
    # Priority queue
    pq = []
    dist = {coord: math.inf for coord in graph.keys()}
    parent = {coord: None for coord in graph.keys()}
    dist[start] = 0
    heapq.heappush(pq, (start, 0))

    while pq:
        u, d = heapq.heappop(pq)

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

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (v, dist[v]))

    return -1, []


def get_direction(pos1: Coordinate, pos2: Coordinate) -> Coordinate:
    return Coordinate(
        (pos2.x - pos1.x) // abs(pos2.x - pos1.x) if pos2.x != pos1.x else 0,
        (pos2.y - pos1.y) // abs(pos2.y - pos1.y) if pos2.y != pos1.y else 0,
    )


def print_tunnel(tunnel: List[List[str]]) -> None:
    for row in tunnel:
        print("".join(row))


def plot_tunnel(
    walls: List[LineString],
    edges: List[LineString],
    path: List[LineString],
) -> None:
    """
    Plots the tunnel

    Args:
        walls: List of LineString representing walls of the tunnel
        edges: List of LineString representing all connections between corners
        path: List of LineString representing the shortest path between start and end
    """
    _, ax = plt.subplots()

    for wall in walls:
        plot_line(wall, ax=ax, color="blue")

    for edge in edges:
        plot_line(edge, ax=ax, color="red")

    for p in path:
        plot_line(p, ax=ax, color="green", linewidth=3)

    plt.show()


def parse_file(file_name: str) -> Tuple[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    instructions = []
    with open(abs_file_path, "r") as f:
        instructions = f.read().strip().split(",")
    return instructions


part1()
part2()
part3()
