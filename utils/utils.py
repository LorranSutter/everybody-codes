from typing import List, Optional, Union

import matplotlib.pyplot as plt


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\x1b[6;30;42m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


class tcolors:
    BLACK = "\33[30m"
    RED = "\33[31m"
    GREEN = "\33[32m"
    YELLOW = "\33[33m"
    BLUE = "\33[34m"
    VIOLET = "\33[35m"
    BEIGE = "\33[36m"
    WHITE = "\33[37m"
    RESET = "\033[0m"


def print_matrix(
    matrix: List[List[Union[str, int, float]]], sep: str = "", min_width: int = 0
):
    """Print a 2D matrix, one row per line.

    Args:
        matrix: Rows of values to print.
        sep: String inserted between elements in a row.
        min_width: Minimum width each element is right-justified to.
    """
    for row in matrix:
        print(sep.join(str(elem).rjust(min_width) for elem in row))


def plot_points(
    points: List[Union[int, float]],
    points2: Optional[List[Union[int, float]]] = None,
    points2_x: Optional[List[Union[int, float]]] = None,
    title: str = "",
):
    """Plot one or two lists of values as a 2D scatter, with a grid.

    Args:
        points: Y values, plotted against X = 1..len(points).
        points2: Optional second set of Y values, plotted in a different color
            on the same figure.
        points2_x: X coordinates for points2. Defaults to 1..len(points2) if
            not given.
        title: Optional plot title.
    """
    plt.figure()
    plt.scatter(range(1, len(points) + 1), points, color="tab:blue")
    if points2 is not None:
        x2 = points2_x if points2_x is not None else range(1, len(points2) + 1)
        plt.scatter(x2, points2, color="tab:red")
    if title:
        plt.title(title)
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()
