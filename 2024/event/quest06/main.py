import os
from collections import defaultdict
from typing import Dict, List

from utils.timer import timer

"""
Preprocessing:
- The problem talks about a tree of apples, so naturally we used a tree to store the data — just a
  plain dictionary, actually, mapping each branch name to the list of branches or fruits it connects to.

Part 1:
- I have to say I misread the description a couple of times before I understood what was asked, and I'd
  say the majority of the work for this whole quest was here in part 1.
- The key realisation is that every fruit shares its path length to the root with other fruits, except
  for exactly one — that lone fruit, the one with a unique-length path, is the powerful one we want.
- So we just perform a DFS over the whole tree, keeping track of the path we are traversing. When we
  reach a fruit ('@'), we save a copy of the current path to a list, and also bump a dictionary that
  counts how many paths have length X.
- After the DFS, we just look for the path whose length has a count of 1 in that dictionary, and
  return it as the answer.

Part 2:
- Pretty much the same thing as part 1, but instead of returning the whole path, we just concatenate
  the first letter of each node.

Part 3:
- I have to say I got quite surprised that the solution to part 3 required only 2 extra lines of code.
- The BUGs and ANTs added to the notes point at each other, so the DFS falls into infinite loops. In
  our input, `BUG:ANT,ANT,BUG,BUG` and `ANT:BUG,@` reference each other directly:

      BUG ──> ANT ──> BUG ──> ANT ──> ...     (and BUG even lists itself as one of its children)

- The fix was simple: just bail out of the DFS the moment we land on an "ANT" or "BUG" node, so we
  never follow their connections and never count the fake '@' dangling off ANT.
"""


@timer
def part1():
    tree = parse_file("input01.txt")

    path = most_powerful_fruit_branch(tree)
    path = "".join(path)

    print(f"Most powerful fruit path: {path}")


@timer
def part2():
    tree = parse_file("input02.txt")

    path = most_powerful_fruit_branch(tree)
    path = "".join((p[0] for p in path))

    print(f"Most powerful fruit path: {path}")


@timer
def part3():
    tree = parse_file("input03.txt")

    path = most_powerful_fruit_branch(tree)
    path = "".join((p[0] for p in path))

    print(f"Most powerful fruit path: {path}")


def most_powerful_fruit_branch(tree: Dict[str, List[str]]) -> List[str]:
    fruit_paths = []
    fruit_path_lengths = defaultdict(int)

    def dfs(node: str, path: List[str]):
        nonlocal fruit_paths
        path.append(node)

        if node in ["ANT", "BUG"]:
            return
        if node == "@":
            fruit_paths.append(path[:])
            fruit_path_lengths[len(path)] += 1
            return

        for child in tree[node]:
            dfs(child, path)
            path.pop()

    dfs("RR", [])

    most_powerful = []
    for fruit_path in fruit_paths:
        if fruit_path_lengths[len(fruit_path)] == 1:
            most_powerful = fruit_path
            break

    return most_powerful


def parse_file(file_name: str) -> Dict[str, List[str]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    tree = defaultdict(str)
    with open(abs_file_path, "r") as f:
        for line in f:
            source, destinies = line.strip().split(":")
            destinies = destinies.split(",")
            tree[source] = destinies
    return tree


part1()
part2()
part3()
