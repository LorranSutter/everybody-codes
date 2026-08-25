from typing import List, Union


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
