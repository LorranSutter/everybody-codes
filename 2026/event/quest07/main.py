import os
import re
from dataclasses import dataclass
from collections import deque

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
class Cloud:
    ID: int
    energy: int
    connections: list[int]
    exploded: bool = False


def calculate_total_energy(graph: dict[int, Cloud], start_energy: int) -> int:
    start = 0
    max_connections = 0
    for cloud_id in graph.keys():
        if len(graph[cloud_id].connections) > max_connections:
            max_connections = len(graph[cloud_id].connections)
            start = cloud_id

    graph[start].energy += start_energy

    queue = deque([(start, start_energy - 1)])
    while queue:
        cloud_id, impulse = queue.popleft()

        for ID in graph[cloud_id].connections:
            graph[ID].energy += impulse

            if impulse > 1:
                queue.append((ID, impulse - 1))

    return sum(graph[i].energy for i in graph)


@timer
def part1():
    graph = parse_file("input01.txt")
    start_energy = 5

    total_energy = calculate_total_energy(graph, start_energy)

    print(f"Total energy after propagating: {total_energy}")


@timer
def part2():
    graph = parse_file("input02.txt")
    start_energy = 10

    total_energy = calculate_total_energy(graph, start_energy)

    print(f"Total energy after propagating: {total_energy}")


@timer
def part3():
    # TODO: Implement part 3
    pass


def parse_file(file_name: str) -> dict[int, Cloud]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    graph: dict[int, Cloud] = dict()
    with open(abs_file_path, "r") as f:
        for line in f:
            ID, energy, connections = re.findall(
                r"id=(\d+),\senergy=(\d+),\sconnections=([\d,\s]+)", line.strip()
            )[0]

            ID, energy, connections = (
                int(ID),
                int(energy),
                list(map(int, connections.split(","))),
            )

            graph[ID] = Cloud(ID, energy, connections)

    return graph


part1()
part2()
# part3()
