import os
from collections import defaultdict
from typing import Set, Tuple

from utils.timer import timer

"""
Preprocessing:
- Read the input file and return a list of names and a dictionary of rules.
- We have the is_prefix_valid function that checks if a string is a valid prefix
    - If gets the first letter of the string and checks if it exists in the rules.
    - If it does, check the next letter against the list of letters associated with the last letter.
    - If we finish the string, it is a valid prefix.

Part 1:
- Iterate through the names and check which one is a valid name.

Part 2:
- Iterate through the names and check which ones are valid.
- Return the sum of the indexes of the valid names.

Part 3:
- Iterate through the prefixes and check which ones are valid.
    - If a name is valid, we perform a DFS to find all valid names this prefix can create.
    - A valid name must have the size between min_size and max_size.
    - Since we can have duplicated valid names, we store them in a set.
    - The total number of valid names is the size of the set.
"""


@timer
def part1():
    names, rules = parse_file("input01.txt")

    name_created = ""
    for name in names:
        if is_prefix_valid(name, rules):
            name_created = name
            break

    print("The name that can be created is:", name_created)


@timer
def part2():
    names, rules = parse_file("input02.txt")

    name_ids = 0
    for i, name in enumerate(names, 1):
        if is_prefix_valid(name, rules):
            name_ids += i

    print("Sum of the indices that comply with the rules:", name_ids)


@timer
def part3():
    names, rules = parse_file("input03.txt")
    min_size = 7
    max_size = 11

    name_set = set()
    for prefix in names:
        if is_prefix_valid(prefix, rules):
            letter = prefix[-1]

            name_size = len(prefix)
            name = prefix
            if name_size > max_size:
                continue

            print("Prefix:", name)
            name_set.add(name)
            new_names = dfs(name, letter, rules, min_size, max_size, name_set)
            name_set.update(new_names)

    print("Number of unique names:", len(name_set))


def is_prefix_valid(name: str, rules: dict) -> bool:
    available_letters = rules.keys()
    for letter in name:
        if letter not in available_letters:
            return False
        available_letters = rules[letter]

    return True


def dfs(
    name: str,
    letter: str,
    rules: defaultdict,
    min_size: int,
    max_size: int,
    name_set: Set[str],
) -> Set[str]:
    for l in rules[letter]:
        new_size = len(name) + 1
        if min_size <= new_size <= max_size:
            name_set.add(name + l)
            dfs(name + l, l, rules, min_size, max_size, name_set)
        elif new_size < min_size:
            dfs(name + l, l, rules, min_size, max_size, name_set)

    return name_set


def parse_file(file_name: str) -> Tuple[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    names = []
    rules = defaultdict(list)
    with open(abs_file_path, "r") as f:
        names, rules_str = f.read().strip().split("\n\n")

        names = names.split(",")

        for rule in rules_str.split("\n"):
            source, letters = rule.split(">")
            source = source.strip()
            letters = letters.strip().split(",")

            if rules[source] == []:
                rules[source] = letters
            else:
                rules[source].extend(letters)

    return names, rules


part1()
part2()
part3()
