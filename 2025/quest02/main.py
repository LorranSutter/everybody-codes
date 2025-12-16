import os
import re
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

"""
Preprocessing:
- Just get the two integers of the A point in the file.

Part 1:
- Simple iteration of 3 cycle of operations.

Part 2:
- Same as part 1, but we do 100 cycles and we use each point of the grid as point of examination.

Part 3:
- Same as part 1, but with a 1001x1001 grid.
"""


def part1():
    A = parse_file("input01.txt")
    R = tuple([0, 0])

    for _ in range(3):
        R = mul(R, R)
        R = div(R, tuple([10, 10]))
        R = add(R, A)

    formatted_result = f"[{R[0]},{R[1]}]"
    print("Final result:", formatted_result)


def part2():
    A = parse_file("input_sample02.txt")
    size = 101
    step = 10
    engrave = size * size
    grid = [["X" for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            P = add(A, tuple([i * step, j * step]))
            R = tuple([0, 0])
            for _ in range(100):
                R = mul(R, R)
                R = div(R, tuple([100000, 100000]))
                R = add(R, P)

                if abs(R[0]) > 1000000 or abs(R[1]) > 1000000:
                    engrave -= 1
                    grid[j][i] = "."
                    break

    plot_grid(grid)

    print("Total engraved points:", engrave)


def part3():
    A = parse_file("input03.txt")
    size = 1001
    engrave = size * size
    grid = [["X" for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            # Step is 1
            P = add(A, tuple([i, j]))
            R = tuple([0, 0])
            for _ in range(100):
                R = mul(R, R)
                R = div(R, tuple([100000, 100000]))
                R = add(R, P)

                if abs(R[0]) > 1000000 or abs(R[1]) > 1000000:
                    engrave -= 1
                    grid[j][i] = "."
                    break

    plot_grid(grid)

    print("Total engraved points:", engrave)


def add(n1: Tuple[int, int], n2: Tuple[int, int]) -> Tuple[int, int]:
    return (n1[0] + n2[0], n1[1] + n2[1])


def mul(n1: Tuple[int, int], n2: Tuple[int, int]) -> Tuple[int, int]:
    return (n1[0] * n2[0] - n1[1] * n2[1], n1[0] * n2[1] + n1[1] * n2[0])


def div(n1: Tuple[int, int], n2: Tuple[int, int]) -> Tuple[int, int]:
    # If we use the // operator, we lose precision for large numbers
    return (int(n1[0] / n2[0]), int(n1[1] / n2[1]))


def plot_grid(grid: List[List[str]]):
    x_range = range(len(grid))
    y_range = range(len(grid[0]))
    X, Y = np.meshgrid(x_range, y_range)

    all_points_x = X.flatten()
    all_points_y = Y.flatten()

    specific_points_x = []
    specific_points_y = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "X":
                specific_points_x.append(i)
                specific_points_y.append(j)

    ax = plt.gca()
    ax.scatter(
        all_points_x,
        all_points_y,
        color="grey",
        marker="o",
        s=1,
        label="All Grid Points",
    )
    ax.scatter(
        specific_points_x,
        specific_points_y,
        color="red",
        marker="o",
        s=10,
        label="Specific Points",
        zorder=10,
    )

    plt.grid(True, linestyle="--", alpha=0.6)

    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Visualization of Grid Points")
    plt.show()


def parse_file(file_name: str) -> Tuple[int, int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    A = tuple()
    with open(abs_file_path) as f:
        pattern = r"\w=\[(-*\d+),(-*\d+)\]"
        line = f.readline().strip()
        match = re.search(pattern, line)
        A = tuple(map(int, match.groups()))

    return A


part2()
