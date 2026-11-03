import os
from collections import deque

from utils.timer import timer

"""
Preprocessing:
- Each record becomes one entry in a dict, `item -> [ingredients]`, which is just an adjacency list of a directed
  graph. Basic ingredients never show up on the left-hand side, so they're simply not keys. That's how every part
  spots a leaf: `ingredient not in graph.keys()` means there's nothing further to expand.

Part 1:
- This is a plain BFS starting at `NULL` and walking ingredient edges. The only trick is that the graph has cycles,
  so we need a `visited` set to avoid looping forever, and that same set doubles as our list of distinct ingredients.
- We seed `visited` with `NULL` itself. That way a chain that loops back to it (like `MLKK -> NULL` in the example)
  doesn't get expanded again, and the answer is `len(visited) - 1` to leave `NULL` out of the count.
- Basic ingredients still go into `visited` (they count), we just don't try to expand them.

Part 2:
- Now the question is flipped: instead of "what does `NULL` use?" it's "what uses `NULL`?". We answer it with
  the same BFS as part 1, but run once from every product, stopping as soon as we bump into `NULL`.
- The early `break` is what keeps this cheap enough: most products that use `NULL` hit it within a few levels, so we
  rarely explore a whole subgraph. Still, it's a little bit brute force.
- Seeding each search's `visited` with the product itself has a nice side effect: `NULL`'s own search can never
  reach `NULL` again, so `NULL` doesn't count itself as a product that uses it.
- Alternative approach: reverse every edge (`ingredient -> [items that use it]`) and run a single BFS from `NULL`.
  Everything it reaches is a product that uses `NULL`, and we skip one search per product.

Part 3:
- Same per-product BFS as part 2, but now `NULL` comes in three flavours (`NULLv1`, `NULLv2`, `NULLv3`). Instead of
  stopping at the first `NULL`, we collect every distinct version we meet in a set, and only once it holds two of them
  do we flag the product and `break`.
- `ingredient.startswith("NULL")` catches all three versions without listing them. Since a version reached through
  several chains is still the same version, the set makes sure it's only counted once.
- Alternative approach: with the reversed graph from part 2, run one BFS per version and count how many times each
  product gets reached. Anything reached by two or more of the three searches is contaminated.
"""


@timer
def part1():
    graph = parse_file("input01.txt")

    queue = deque(graph["NULL"])
    visited = set(["NULL"])
    while queue:
        ingredient = queue.popleft()

        visited.add(ingredient)
        if ingredient not in graph.keys():
            continue

        for item in graph[ingredient]:
            if item not in visited:
                queue.append(item)

    print(f"Total ingredients to make NULL: {len(visited) - 1}")


@timer
def part2():
    graph = parse_file("input02.txt")

    contaminated = set()
    for product in graph.keys():
        queue = deque(graph[product])
        visited = set([product])
        while queue:
            ingredient = queue.popleft()

            if ingredient == "NULL":
                contaminated.add(product)
                break

            visited.add(ingredient)
            if ingredient not in graph.keys():
                continue

            for item in graph[ingredient]:
                if item not in visited:
                    queue.append(item)

    print(f"Total contaminated products: {len(contaminated)}")


@timer
def part3():
    graph = parse_file("input03.txt")

    contaminated = set()
    for product in graph.keys():
        potentially_contaminated = set()
        queue = deque(graph[product])
        visited = set([product])
        while queue:
            ingredient = queue.popleft()

            if ingredient.startswith("NULL"):
                potentially_contaminated.add(ingredient)
                if len(potentially_contaminated) >= 2:
                    contaminated.add(product)
                    break

            visited.add(ingredient)
            if ingredient not in graph.keys():
                continue

            for item in graph[ingredient]:
                if item not in visited:
                    queue.append(item)

    print(f"Total contaminated products: {len(contaminated)}")


def parse_file(file_name: str) -> dict[str, list[str]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    graph = dict()
    with open(abs_file_path, "r") as f:
        for line in f:
            item, ingredients = line.strip().split(":")
            graph[item] = ingredients.split(",")
    return graph


part1()
part2()
part3()
