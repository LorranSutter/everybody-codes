import os
import re
from typing import List

from utils.timer import timer

"""
Preprocessing:
- Read the input file and split every parameter using regex

Part 1:
- Normal simulation of the eni function for all parameters

Part 2:
- The normal simulation would take impractical time, so we found a more efficient method using modular exponentiation and the Python pow function.
    - The eni formula is as follows:
        a * N mod M = r1
        r1 * N mod M = r2
        ...
        r_(EXP-1) * N mod M = r_EXP
    - If we replace the first equation into the second equation, we get:
        (a * N mod M) * N mod M = r2
        a * N^2 mod M = r2
    - If we continue the process, we get the general formula:
        a * N^EXP mod M = r_EXP
- Since the quest requires only the last 5 remainders, we can use the pow function to calculate it:
    - pow(A, X, M), pow(A, X-1, M), ..., pow(A, X-4, M)

Part 3:
- Again, a normal simulation would be too slow, so we realized a pattern in the eni function:
    - Considering we always do a mod M, it means all remainders would range from 0 to M-1
    - It means, for a long execution, there is a good chance that the remainders start repeating after a certain point.
    - So the goal here is to find where the cycle starts and skip further executions.
- The final result is the sum of 3 steps:
    - The sum of the remainders before the cycle starts
    - The sum of the remainders in the cycle
    - The sum of the remainders after the cycle ends
"""


@timer
def part1():
    params = parse_file("input01.txt")

    max_result = 0
    for param in params:
        A, B, C, X, Y, Z, M = param

        result = eni(A, X, M) + eni(B, Y, M) + eni(C, Z, M)

        if result > max_result:
            max_result = result

    print(f"Highest result:", max_result)


@timer
def part2():
    params = parse_file("input02.txt")

    max_result = 0
    for param in params:
        A, B, C, X, Y, Z, M = param

        result = eni_pow(A, X, M, 5) + eni_pow(B, Y, M, 5) + eni_pow(C, Z, M, 5)

        if result > max_result:
            max_result = result

    print(f"Highest result:", max_result)


@timer
def part3():
    params = parse_file("input03.txt")

    max_result = 0
    for i, param in enumerate(params):
        A, B, C, X, Y, Z, M = param

        result = eni_sum(A, X, M) + eni_sum(B, Y, M) + eni_sum(C, Z, M)

        if result > max_result:
            max_result = result
        
        print(f"({i+1}/{len(params)}) Partial result: {result} Max result: {max_result}")

    print(f"Highest result:", max_result)


def eni(N: int, EXP: int, MOD: int) -> int:
    score = 1
    remainders = ""
    for _ in range(EXP):
        score = (score * N) % MOD
        remainders = str(score) + remainders

    return int(remainders)


def eni_pow(N: int, EXP: int, MOD: int, num_remainders: int) -> int:
    result = []
    for i in range(EXP, EXP - num_remainders, -1):
        result.append(str(pow(N, i, MOD)))

    if EXP < num_remainders:
        return int("".join(result[:EXP]))
    return int("".join(result))


def eni_sum(N: int, EXP: int, MOD: int) -> int:
    score = 1
    remainders = []
    for _ in range(EXP):
        score = (score * N) % MOD

        # Found the start of the cycle
        if score in remainders:
            break

        remainders.append(score)

    # Find the index of the cycle start
    cycle_start_index = remainders.index(score)

    # Total number of cycles
    num_cycles = EXP // (len(remainders[cycle_start_index:])) - len(
        remainders[:cycle_start_index]
    )

    # Remaining remainders to calculate, after the cycles
    remaining = (
        EXP
        - len(remainders[:cycle_start_index])
        - num_cycles * len(remainders[cycle_start_index:])
    )

    return (
        sum(remainders[:cycle_start_index]) # Before the cycle
        + sum(remainders[cycle_start_index:]) * num_cycles # In the cycle
        + sum(remainders[cycle_start_index : cycle_start_index + remaining]) # After the cycle
    )


def parse_file(file_name: str) -> List[List[int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    params = []
    with open(abs_file_path, "r") as f:
        for line in f:
            params.append(map(int, (re.findall(r"=(\d+)", line))))
    return params


# part1()
# part2()
part3()
