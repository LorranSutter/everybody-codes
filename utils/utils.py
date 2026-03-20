from typing import List

def print_matrix(matrix: List[List[str]]):
    for row in matrix:
        print("".join(row))