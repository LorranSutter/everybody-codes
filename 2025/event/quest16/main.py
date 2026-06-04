import os
import math
from typing import List

from utils.timer import timer

"""
Preprocessing:
Read the input file and parse into a list of integers.

Part 1:
- Given a list of spell numbers and the number of columns, calculate how many blocks are needed.
- The key insight is that this is O(n) - we only need the spells and number of columns.
- For each spell number s, the number of blocks placed is: floor(num_cols / s)

    Example:
        Spells: [1, 2, 3, 5, 9]
        Columns: 90
        
        Spell 1: 90/1 = 90 blocks (every column)
        Spell 2: 90/2 = 45 blocks (every 2nd column)
        Spell 3: 90/3 = 30 blocks (every 3rd column)
        Spell 5: 90/5 = 18 blocks (every 5th column)
        Spell 9: 90/9 = 10 blocks (every 9th column)
        
        Total: 90 + 45 + 30 + 18 + 10 = 193 blocks

Part 2:
- Reverse engineer spells from block counts
- Given the number of blocks in each column, determine which spells created the pattern.
- Uses a sieve-like algorithm:
    1. Start with the first column's block count
    2. If count > 0, this index is a spell number
    3. Subtract 1 from all columns at multiples of this index
    4. Move to next column and repeat

    Example:
        Input: [1,2,2,2,2,3,1,2,3,3,1,3,1,2,3,2,1,4,1,3,2,2,1,3,2,2]
        
        Step 1: blocks[0]=1 > 0 → spell=1, subtract 1 from all columns
            [0,1,1,1,1,2,0,1,2,2,0,2,0,1,2,1,0,3,0,2,1,1,0,2,2,1]
        
        Step 2: blocks[1]=1 > 0 → spell=2, subtract 1 from every 2nd column
            [0,0,1,0,1,1,0,0,2,1,0,1,0,0,2,0,0,2,0,1,1,0,0,1,2,0]
        
        Step 3: blocks[2]=1 > 0 → spell=3, subtract 1 from every 3rd column
            [0,0,0,0,1,0,0,0,2,1,0,0,0,0,2,0,0,1,0,1,1,0,0,0,2,0]
        
        Continue until all blocks processed...
        
        Spells found: [1, 2, 3, 5, 9]
        Product: 1 × 2 × 3 × 5 × 9 = 270

Part 3:
- Calculate wall length from total blocks
- Given total blocks available, find the maximum number of complete columns that can be built.
- Mathematical approach using the relationship between blocks (b), columns (C), and spells (s):

    From Part 1, we know:
        b = C/s₁ + C/s₂ + ... + C/sₙ
        b = C × (1/s₁ + 1/s₂ + ... + 1/sₙ)
        b/C = K, where K = Σ(1/sᵢ) is constant for given spells

    Therefore:
        C = b/K

    Example:
        Spells: [1, 2, 3, 5, 9]
        Available blocks: 202520252025000
        
        K = 1/1 + 1/2 + 1/3 + 1/5 + 1/9
            = 1 + 0.5 + 0.333... + 0.2 + 0.111...
            ≈ 2.144...
        
        Initial estimate: C = 202520252025000 / 2.144... ≈ 94439495762953.x
        
        Since only complete columns count, start with floor(C) and increment
        until calc_blocks(spells, C+1) > available_blocks
"""


@timer
def part1():
    spells = parse_file("input01.txt")
    num_cols = 90

    total = calc_blocks(spells, num_cols)

    print(f"Total blocks need to build the wall: {total}")


@timer
def part2():
    blocks = parse_file("input02.txt")
    num_cols = len(blocks)

    spells = calc_spells(blocks, num_cols)

    print(f"Spells used: {spells}")
    print(f"Product of spells that generated the wall: {math.prod(spells)}")


@timer
def part3():
    blocks = parse_file("input03.txt")
    num_cols = len(blocks)
    num_blocks = 202520252025000

    spells = calc_spells(blocks, num_cols)
    print(f"Spells used: {spells}")

    K = sum(1 / spell for spell in spells)

    num_cols = int(num_blocks / K)
    while calc_blocks(spells, num_cols + 1) <= num_blocks:
        num_cols += 1

    print(f"Number of wall colums: {num_cols}")


def calc_blocks(spells: List[int], num_cols: int) -> int:
    return sum(num_cols // spell for spell in spells)


def calc_spells(blocks: List[int], num_cols: int) -> List[int]:
    spells = []
    for i, block in enumerate(blocks, 1):
        if block > 0:
            for j in range(i - 1, num_cols, i):
                blocks[j] -= 1
            spells.append(i)

    return spells


def parse_file(file_name: str) -> List[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    with open(abs_file_path, "r") as f:
        return list(map(int, f.read().strip().split(",")))


part1()
part2()
part3()
