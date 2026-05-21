import os
import math
import shapely
import matplotlib.pyplot as plt
from typing import List, Tuple
from collections import defaultdict
from dataclasses import dataclass
from shapely.geometry import LineString, Point
from shapely.plotting import plot_points, plot_line

from utils.timer import timer
from utils.utils import tcolors

"""
Preprocessing:
-

Part 1:
-

Part 2:
-

Part 3:
-
"""


@dataclass
class Thread:
    start: int
    end: int


@timer
def part1():
    nails = parse_file("input01.txt")
    half_len_nails = max(nails) // 2

    count_center = 0
    for i in range(len(nails) - 1):
        if abs(nails[i] - nails[i + 1]) == half_len_nails:
            count_center += 1

    print("Number of times a thread passes through center:", count_center)


# 2924678 - Length and first character correct
@timer
def part2_2():
    # TODO: Implement part 2
    nails = parse_file("input_sample02.txt")
    # nails = list(nails) + [7]
    print(nails)
    max_num = max(nails)
    print(max_num)
    angle_increment = 2 * math.pi / max_num
    print(angle_increment)

    count_egde_intersections = defaultdict(int)
    nail_coords = []
    for i in range(len(nails)):
        x = round(math.sin(angle_increment * i), 2)
        y = round(math.cos(angle_increment * i), 2)
        nail_coords.append(Point(x, y))
        count_egde_intersections[nails[i]] += 2
    
    print(count_egde_intersections)

    threads = []
    intersections = []
    print(len(nails))
    for i in range(len(nails) - 1):
        print(f"{i/len(nails) * 100:.2f}%", end="\r")
        nail1 = nail_coords[nails[i] - 1]
        nail2 = nail_coords[nails[i + 1] - 1]
        new_thread = LineString([nail1, nail2])
        # print(nails[i] - 1, nails[i+1]-1, new_thread)
        plot_line(new_thread, add_points=False)
        
        for thread in threads:
            if new_thread.coords[0] in thread.coords or new_thread.coords[1] in thread.coords:
                continue
            new_intersection = new_thread.intersection(thread)
            if not new_intersection.is_empty:
                # print("New intersection:", new_intersection)
                intersections.append(new_intersection)
                # for thread in threads:
                #     plot_line(thread)
                # plot_line(new_thread, color="green")
                # plot_points(intersections, color="red")
                # plt.show()
        # intersections += new_intersections
        # print("New intersections:", new_intersections)
        # print("Total intersections:", intersections)

        threads.append(new_thread)

    # plot_points(nail_coords)
    print(len(intersections), "intersections found."  )
    plot_points(intersections, color="red")
    plt.show()


@timer
def part2():
    # TODO: Implement part 2
    nails = parse_file("input02.txt")
    print(nails)

    intersections = 0
    for i in range(len(nails) - 1):
        for j in range(i - 1, -1, -1):
            # print(nails[i : i + 2], nails[j : j + 2])
            t1 = sorted([nails[i], nails[i + 1]])
            t2 = sorted([nails[j], nails[j + 1]])
            if overlapping(t1, t2):
                # print(f"{tcolors.GREEN}Intersected{tcolors.RESET}", t1, t2)
                intersections += 1

    print("Total number of knots:", intersections)


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file("input_sample03.txt")
    pass

def overlapping(t1: List[int], t2: List[int]) -> bool:
    if (
        t1[0] == t2[0]
        or t1[1] == t2[1]
        or t1[0] == t2[1]
        or t1[1] == t2[0]
    ):
        return False
    if max(t1[0], t2[0]) <= min(t1[1], t2[1]):
        if t1[0] > t2[0] and t1[1] < t2[1]:
            return False
        if t2[0] > t1[0] and t2[1] < t1[1]:
            return False
        return True
    
    return False

def intersect(t1: Thread, t2: Thread) -> bool:
    # print(t1, t2)
    if (
        t1.start == t2.start
        or t1.end == t2.end
        or t1.start == t2.end
        or t1.end == t2.start
    ):
        print(t1, t2, "here1")
        return False

    # if t1.start > t1.end:
    #     t1 = Thread(t1.end, t1.start)
    # if t2.start > t2.end:
    #     t2 = Thread(t2.end, t2.start)

    if t1.start < t2.start < t1.end:
        print(t1, t2, "here2")
        return True
    if t1.end < t2.start < t1.start:
        print(t1, t2, "here3")
        return True
    if t1.start < t2.end < t1.end:
        print(t1, t2, "here4")
        return True
    if t1.end < t2.end < t1.start:
        print(t1, t2, "here4")
        return True
    print(t1, t2, "here5")
    return False


def parse_file(file_name: str) -> Tuple[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    nails = []
    with open(abs_file_path, "r") as f:
        nails = tuple(map(int, f.readline().strip().split(",")))
    return nails


# part1()
part2()
# part3()
