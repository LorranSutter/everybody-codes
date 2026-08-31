import os
from typing import Dict, List, Tuple
from dataclasses import dataclass

from utils.timer import timer

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
class Chariot:
    label: str
    plan: List[str]
    current_power: int
    total_power: int = 0


@timer
def part1():
    chariots, _ = parse_file("input01.txt")
    plan_size = len(chariots[0].plan)
    segments = 10

    for i in range(segments):
        for chariot in chariots:
            match chariot.plan[i % plan_size]:
                case "+":
                    chariot.current_power += 1
                case "-":
                    chariot.current_power -= 1
            chariot.total_power += chariot.current_power

    chariots.sort(key=lambda c: -c.total_power)
    ranking = "".join(c.label for c in chariots)
    print(f"Ranking: {ranking}")


@timer
def part2():
    chariots, track = parse_file("input_sample02.txt", True)
    plan_size = len(chariots[0].plan)
    loops = 10

    step = 0
    for _ in range(loops):
        for s in track:
            override = s not in ["=", "S"]
            for chariot in chariots:
                match s if override else chariot.plan[step % plan_size]:
                    case "+":
                        chariot.current_power += 1
                    case "-":
                        chariot.current_power -= 1
                chariot.total_power += chariot.current_power
            step += 1

    chariots.sort(key=lambda c: -c.total_power)
    ranking = "".join(c.label for c in chariots)
    print(f"Ranking: {ranking}")


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file("input_sample03.txt")
    pass


def parse_file(file_name: str, track: bool = False) -> Tuple[List[Chariot], str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    chariots = []
    with open(abs_file_path, "r") as f:
        for line in f:
            label, plan = line.strip().split(":")
            chariots.append(Chariot(label, plan.split(","), 10))
    return chariots, parse_track_file("track_" + file_name) if track else ""


def parse_track_file(file_name: str) -> str:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    with open(abs_file_path, "r") as f:
        data = f.read().split("\n")

    m, n = len(data), len(data[0])
    track = data[0][1]
    visited = set([(0, 0), (0, 1)])
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    i, j = 0, 1
    done = False
    while True:
        if done:
            break

        for di, dj in directions:
            i, j = i + di, j + dj

            if i < 0 or j < 0 or i >= m or j >= n:
                i, j = i - di, j - dj
                continue

            if data[i][j] == "S":
                track += data[i][j]
                done = True
                break

            if (i, j) in visited or data[i][j] == " ":
                i, j = i - di, j - dj
                continue

            visited.add((i, j))
            track += data[i][j]
            break

    return track


part1()
part2()
# part3()
