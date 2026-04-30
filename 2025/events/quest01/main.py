import os
from typing import Tuple

from utils.timer import timer


"""
Preprocessing:
1. Read the input file and parse name and instructions.
2. Parse the instructions into a list of integers. R is a positive int and L is a negative int.

Part 1:
- We just have to know the final position after executing all instructions.
- Iterate through the instructions and update the position accordingly, adding the instruction to the current position.
- We just limit the position to be >= 0 and < length of names.
- Output the name of the final position.

Part 2:
- We also just have to know the final position after executing all instructions.
- Now we don't have to worry about going out of bounds.
- So we just have to calculate the position mod the length of names.
- Output the name of the final position.

Part 3:
- Same as part 1, but after calculating the position, we swap the position 0 with the calculated position.
- Output the name of the final position.
"""


@timer
def part1():
    names, instructions = parse_file("input01.txt")
    l_names = len(names)

    position = 0
    for i in range(len(instructions)):
        position += instructions[i]
        if position >= l_names:
            position = l_names - 1
        elif position < 0:
            position = 0

    print("My name is", names[position])


@timer
def part2():
    names, instructions = parse_file("input02.txt")
    l_names = len(names)

    position = 0
    for i in range(len(instructions)):
        position = (position + instructions[i]) % l_names

    print("The name of my first parent is", names[position])


@timer
def part3():
    names, instructions = parse_file("input03.txt")
    l_names = len(names)

    position = 0
    for i in range(len(instructions)):
        position = (position + instructions[i]) % l_names
        names[0], names[position] = names[position], names[0]
        position = 0

    print("The name of my second parent is", names[position])


def parse_file(file_name: str) -> Tuple[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    names = []
    instructions = []
    with open(abs_file_path) as f:
        names = f.readline().strip().split(",")

        f.readline()  # Skip the blank line

        instructions = f.readline().strip().split(",")
        for i in range(len(instructions)):
            if instructions[i][0] == "R":
                instructions[i] = int(instructions[i][1:])
            else:
                instructions[i] = -int(instructions[i][1:])

    return names, instructions


part3()
