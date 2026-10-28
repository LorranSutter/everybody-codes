import os
from collections import defaultdict, deque

from utils.timer import timer

"""
Note:
- It was hard to visualize a topological sort here at first glance. My initial idea was a big custom sorting function
  that would read all of the alloy comparisons and store them, so the sort could look up each compared pair. I must
  have done it the wrong way, because it didn't work.
- Then I thought this looked like some sort of decision tree, but I couldn't come up with a way to implement it.
- Finally, thinking about the tree, the idea of a directed graph came to mind.

Preprocessing:
- Each line is one group, so we split it by whitespace into tokens like "3>5". Every token unpacks into
  (a, sign, b), which only works because the alloy ids are single characters.

Part 1:
- The key insight is that this is a directed graph: every harder alloy points to the softer ones. The hardest alloy
  is the one with 0 edges pointing to it, and the softest is the one with the most.
- So we build the graph, flipping the edge when the sign is "<" so it always goes hard -> soft. Then we run a
  topological sort (Kahn's algorithm): count the in-degrees, start from the alloys with 0, and every time we pop one
  we remove its edges and enqueue the neighbours that dropped to 0. The pop order is the hardest-to-softest order.
- Joining the ids gives the group's number, and the sum of all groups is the checksum.

Part 2:
- Same as part 1, nothing to change. With one comparison missing we never have to deduce it, because the missing
  edge is always implied by a path through other alloys (1 > 2 > 3 already forces 1 > 3). Kahn's algorithm only
  needs the edges that keep the order unique, so it comes out the same.

Part 3:
- Same as part 1 again. Even with many comparisons gone, the statement guarantees the remaining ones are enough to
  fix a single order. That means there is always exactly one alloy with in-degree 0 at each step, so the queue never
  has a tie to break.
"""


@timer
def part1():
    compare_list = parse_file("input01.txt")

    checksum = calculate_checksum(compare_list)
    print(f"Final checksum: {checksum}")


@timer
def part2():
    compare_list = parse_file("input02.txt")

    checksum = calculate_checksum(compare_list)
    print(f"Final checksum: {checksum}")


@timer
def part3():
    compare_list = parse_file("input03.txt")

    checksum = calculate_checksum(compare_list)
    print(f"Final checksum: {checksum}")


def calculate_checksum(compare_list: list[list[str]]) -> int:
    checksum = 0
    for compare in compare_list:
        graph = create_graph(compare)
        alloys = topological_sort(graph)
        checksum += int("".join(alloys))

    return checksum


def create_graph(compares: list[str]) -> dict[str, set[str]]:
    graph = defaultdict(set)
    for compare in compares:
        a, sign, b = compare

        if sign == ">":
            graph[a].add(b)
            if b not in graph:
                graph[b] = set()
        else:
            graph[b].add(a)
            if a not in graph:
                graph[a] = set()

    return graph


def topological_sort(graph: dict[str, set[str]]) -> list[str]:
    in_degrees = {key: 0 for key in graph.keys()}
    for source in graph.keys():
        for node in graph[source]:
            in_degrees[node] += 1

    queue = deque([u for u in graph.keys() if in_degrees[u] == 0])

    result = []
    while queue:
        u = queue.popleft()
        result.append(u)

        for v in graph[u]:
            in_degrees[v] -= 1
            if in_degrees[v] == 0:
                queue.append(v)

    return result


def parse_file(file_name: str) -> list[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    compares = []
    with open(abs_file_path, "r") as f:
        for line in f:
            compares.append(line.strip().split())
    return compares


part1()
part2()
part3()
