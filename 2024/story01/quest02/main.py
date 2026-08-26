import os
import re
from typing import List, Tuple
from dataclasses import dataclass
from collections import deque, Counter

from utils.timer import timer

"""
Preprocessing:
- A couple of dataclasses to represent the Node information, Command information, and Instruction information (this is each row of the input file).
- We also create a TreeNode class to represent the tree structure, that has functions to help in each part of the problem.
- We read the input file and parse it into a list of Instruction objects.

Part 1:
- We create the tree structure inserting each node like a normal binary tree.
- The trick here is that everytime we insert a node, we also record the level of the node:
    Tree     Level
    P        0
    B L      1
    R H T M  2
- After inserting each node, we call the find_message function that do the following:
    - Perform a BFS to gather the nodes in level-order traversal
    - Gets the counter of how many nodes there are at each level
    - The BFS is necessary here because the order how we read each level is important.
- Having the nodes in level-rder traversal and the most common level, we can return the message

Part 2:
- Same as part 1, but we have the SWAP command now.
- Every time we receive a SWAP command, we perform a DFS to find the corresponding node by the ID.
- Since we just have to change the information of the nodes, we just we just update the rank and symbol of the left and right nodes.
- Then, we call the find_message function to get the new message.

Part 3:
- Here, since we have to swap the whole branch, the process is a bit different from part 2.
- We don't just perform a simple DFS to fiind the node by the ID. Instead, we return the parent of the nodes to be swapped.
- Also, since it is a binary tree, we have to mind if the nodes are on the left or the right and perform the swap accordingly.
- The trick to save the levels during insertion does not work here anymore, so we have to update the levels of each node after all insertions and swaps.
- Then, we can call the find_message function to get the new message.
"""


@dataclass
class Node:
    rank: int
    symbol: str


@dataclass
class Command:
    command: str
    id: int


@dataclass
class Instruction:
    command: Command
    id: int
    left: Node
    right: Node


class TreeNode:
    def __init__(self, id: int, rank: int, symbol: str, level: int = 0) -> None:
        self.id = id
        self.rank = rank
        self.symbol = symbol
        self.level = level
        self.left = None
        self.right = None

    def insert(self, id: int, rank: int, symbol: str) -> None:
        """
        Insert a new node into the tree at the appropriate position based on the rank
        """
        if rank < self.rank:
            if self.left is None:
                self.left = TreeNode(id, rank, symbol, self.level + 1)
            else:
                self.left.insert(id, rank, symbol)
        else:
            if self.right is None:
                self.right = TreeNode(id, rank, symbol, self.level + 1)
            else:
                self.right.insert(id, rank, symbol)

    def get_level_order_nodes(self) -> Tuple[List[int], Counter]:
        """
        Perform a BFS on the tree, and return a list of nodes in level order,
        along with a Counter object that counts the number of nodes at each level
        """
        level_counts = Counter()

        if not self:
            return []

        queue = deque([self])
        result = []
        while queue:
            node = queue.popleft()

            level_counts[node.level] += 1
            result.append(node)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result, level_counts

    def search(self, id: int) -> "TreeNode":
        """Use DFS to search a node in the whole tree"""
        if not self:
            return None
        if self.id == id:
            return self

        if self.left:
            left_result = self.left.search(id)
            if left_result:
                return left_result

        if self.right:
            right_result = self.right.search(id)
            if right_result:
                return right_result

        return None

    def search_with_parent(
        self, id: int, result: List[Tuple["TreeNode", str]]
    ) -> List[Tuple["TreeNode", str]]:
        """
        Use DFS to search the node in the whole tree
        There could be more than one node with the same ID, so it returns a list of nodes
        It returns the parent of the intended node and the direction where the node is located (L or R)
        """
        if result is None:
            result = []

        if self.id == id:
            return result

        if self.left and self.left.id == id:
            result += [(self, "L")]
        elif self.right and self.right.id == id:
            result += [(self, "R")]

        if self.left:
            left_result = self.left.search_with_parent(id, result)
            if len(left_result) > 0:
                result = left_result

        if self.right:
            result = self.right.search_with_parent(id, result)

        return result

    def set_levels(self, level: int = 0) -> None:
        """Use DFS to set the level of each node in the tree"""
        if not self:
            return

        self.level = level

        if self.left:
            self.left.set_levels(level + 1)
        if self.right:
            self.right.set_levels(level + 1)

    def find_message(self) -> str:
        tree_array, counter = self.get_level_order_nodes()

        # There is a chance that more than one level has the most number of nodes
        # In this case, we select the level closest to the root level
        most_common_list = sorted(counter.most_common(), key=lambda x: (-x[1], x[0]))
        most_common_level = most_common_list[0][0]

        return "".join(
            [node.symbol for node in tree_array if node.level == most_common_level]
        )

    def print_tree(self) -> None:
        arr, _ = self.get_level_order_nodes()

        current_level = 0
        for item in arr:
            if item.level > current_level:
                print()
                current_level = item.level

            print((item.symbol), end=" ")
        print()


@timer
def part1():
    instructions = parse_file("input01.txt")

    left_tree, right_tree = TreeNode(
        instructions[0].id, instructions[0].left.rank, instructions[0].left.symbol
    ), TreeNode(
        instructions[0].id, instructions[0].right.rank, instructions[0].right.symbol
    )

    for instruction in instructions[1:]:
        left_tree.insert(instruction.id, instruction.left.rank, instruction.left.symbol)
        right_tree.insert(
            instruction.id, instruction.right.rank, instruction.right.symbol
        )

    left_message = left_tree.find_message()
    right_message = right_tree.find_message()

    print("Left Tree")
    left_tree.print_tree()
    print("Right Tree")
    right_tree.print_tree()
    print(f"Final message: {left_message}{right_message}")


@timer
def part2():
    instructions = parse_file("input02.txt")

    left_tree, right_tree = TreeNode(
        instructions[0].id, instructions[0].left.rank, instructions[0].left.symbol
    ), TreeNode(
        instructions[0].id, instructions[0].right.rank, instructions[0].right.symbol
    )

    for instruction in instructions[1:]:
        if instruction.command.command == "ADD":
            left_tree.insert(
                instruction.id, instruction.left.rank, instruction.left.symbol
            )
            right_tree.insert(
                instruction.id, instruction.right.rank, instruction.right.symbol
            )
        else:
            # SWAP
            left_node = left_tree.search(instruction.command.id)
            right_node = right_tree.search(instruction.command.id)

            left_node.rank, right_node.rank = right_node.rank, left_node.rank
            left_node.symbol, right_node.symbol = right_node.symbol, left_node.symbol

    left_message = left_tree.find_message()
    right_message = right_tree.find_message()

    print("Left Tree")
    left_tree.print_tree()
    print("Right Tree")
    right_tree.print_tree()
    print(f"Final message: {left_message}{right_message}")


@timer
def part3():
    instructions = parse_file("input03.txt")

    left_tree, right_tree = TreeNode(
        instructions[0].id, instructions[0].left.rank, instructions[0].left.symbol
    ), TreeNode(
        instructions[0].id, instructions[0].right.rank, instructions[0].right.symbol
    )

    for instruction in instructions[1:]:
        if instruction.command.command == "ADD":
            left_tree.insert(
                instruction.id, instruction.left.rank, instruction.left.symbol
            )
            right_tree.insert(
                instruction.id, instruction.right.rank, instruction.right.symbol
            )
        else:
            # SWAP
            if instruction.command.id == 1:
                left_tree, right_tree = right_tree, left_tree
                continue

            result_left = left_tree.search_with_parent(instruction.command.id, [])
            result_right = right_tree.search_with_parent(instruction.command.id, [])

            # The nodes to be swapped might be in the same tree
            node_a, node_b = None, None
            node_a_dir, node_b_dir = None, None
            if len(result_left) == 0:  # Both nodes are in the right tree
                node_a = result_right[0][0]
                node_a_dir = result_right[0][1]
                node_b = result_right[1][0]
                node_b_dir = result_right[1][1]
            elif len(result_right) == 0:  # Both nodes are in the left tree
                node_a = result_left[0][0]
                node_a_dir = result_left[0][1]
                node_b = result_left[1][0]
                node_b_dir = result_left[1][1]
            else:  # Nodes are in different trees
                node_a = result_left[0][0]
                node_a_dir = result_left[0][1]
                node_b = result_right[0][0]
                node_b_dir = result_right[0][1]

            if node_a_dir == "L" and node_b_dir == "L":
                node_a.left, node_b.left = (
                    node_b.left,
                    node_a.left,
                )
            elif node_a_dir == "L" and node_b_dir == "R":
                node_a.left, node_b.right = (
                    node_b.right,
                    node_a.left,
                )
            elif node_a_dir == "R" and node_b_dir == "L":
                node_a.right, node_b.left = (
                    node_b.left,
                    node_a.right,
                )
            elif node_a_dir == "R" and node_b_dir == "R":
                node_a.right, node_b.right = (
                    node_b.right,
                    node_a.right,
                )

    left_tree.set_levels()
    right_tree.set_levels()
    left_message = left_tree.find_message()
    right_message = right_tree.find_message()

    print("Left Tree")
    left_tree.print_tree()
    print("Right Tree")
    right_tree.print_tree()
    print(f"Final message: {left_message}{right_message}")


def parse_file(file_name: str) -> List[Instruction]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    left, right = [], []
    instructions = []
    with open(abs_file_path, "r") as f:
        for line in f:
            line = line.strip().split(" ")

            if len(line) == 2:
                instructions.append(
                    Instruction(Command(line[0], int(line[1])), None, None, None)
                )
            else:
                command = Command(line[0], None)
                id = int(re.search(r"(\d+)", line[1]).group(1))
                left = re.findall(r"\[(\d+),(\D+)\]", line[2])
                left_node = Node(int(left[0][0]), left[0][1])
                right = re.findall(r"\[(\d+),(\D+)\]", line[3])
                right_node = Node(int(right[0][0]), right[0][1])

                instructions.append(Instruction(command, id, left_node, right_node))

    return instructions


part1()
part2()
part3()
