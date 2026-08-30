import os
import re
from collections import defaultdict, deque
from typing import Dict, List, Tuple

from utils.timer import timer

"""
Preprocessing:
- Created a directed weighed graph to use as the data structure for this problem
- Each node of the graph represents a plant, that has:
    - id -> id of the plant
    - thickness -> thickness of the plant that interfeers in the brightness
    - energy -> the current accumulated energy of the plant, initially 0
- When we read the file, we add the plant Ids to the graph, along with the thickness
  and set the energy to 0
- When we have a branch, we create an edge between two plants, and the thickness
  is the weight associated.
- To handle the free branches, I created a node 0, that is connected to all
  plants that is defined as free branch. Also, the node 0 is the only one
  that starts with energy 1, otherwise the whole system energy would be 0.

Part 1:
- Here we pretty much perform a topological sort (Kahn's Algorithm), where we find
  the "in degree" of each node initially, that is pretty much the number of connections
  that this node is receiving (the branches). Then we start iterating over the nodes
  with "in degree" 0 similarly to a BFS. Every time we find a new node that is connected
  to the current node in the iteration, we reduce its "in degree". When it is 0,
  we can add it to the queue, so it will be consumed next.
- The adition here is the calculation of the energy in every iteration. We created
  an array called incoming_energy that holds the current energy of each node. 0 for
  everyone except the node 0.
- In every iteration we accumulate the energy in the corresponding node in the incoming_energy
  array. We do that instead of altering the energy property of the node directly, because
  we must have all incoming energy from the connected branches first.
- Once the node reaches "in degree" 0, we check if the incoming energy of this node
  is equal or greather than its thickness. If so, we can set the node energy to the
  calculated value, otherwise, it becomes 0
- At the end of the algorithm, we will have the energy of all plants, so we can
  output the value of the last plant as the answer.

Part 2:
- Pretty much the same simulation from part 1 for several different cases.
- Since we have to activate or not the initial plants, we can simple reuse all
  logic from part 1, just setting the initial weight to 0 when we have to 
  deactivate some plant. After that, we can normaly run the modified topological
  sort algorithm.
- We update the inital weights for all plants, run the algorithm and get the 
  energy of the last plant, and acumulate to the final answer.
- We just have to remember to reset the energy of the plants after every iteration.

Part 3:
-
"""


class PlantNode:
    def __init__(self, node_id: int, thickness: int = 0, energy: int = 0):
        self.id = node_id
        self.thickness = thickness
        self.energy = energy

    def __repr__(self):
        return f"Node(id={self.id}, thickness={self.thickness}, energy={self.energy})"


class DirectedWeightedGraph:
    def __init__(self):
        self.nodes = {}
        self.adj_list = {}

    def add_node(self, node_id: int, thickness: int = 0, energy: int = 0):
        if node_id not in self.nodes:
            self.nodes[node_id] = PlantNode(node_id, thickness, energy)
            self.adj_list[node_id] = {}
        else:
            self.nodes[node_id].thickness = thickness
            self.nodes[node_id].energy = energy

    def add_edge(self, src_id: int, dest_id: int, weight: int):
        if src_id not in self.nodes:
            self.add_node(src_id)
        if dest_id not in self.nodes:
            self.add_node(dest_id)

        self.adj_list[src_id][dest_id] = weight

    def get_node_values(self, node_id: int) -> Tuple[int, int]:
        if node_id in self.nodes:
            return self.nodes[node_id].thickness, self.nodes[node_id].energy
        return None

    def get_neighbors(self, node_id: int) -> List[Dict[int, int]]:
        return self.adj_list.get(node_id, {})

    def get_weight(self, src_id: int, dest_id: int) -> int:
        if src_id not in self.nodes:
            return 0
        if dest_id not in self.nodes:
            return 0
        return self.adj_list[src_id][dest_id]

    def display(self):
        for node_id, node_obj in self.nodes.items():
            edges = self.adj_list[node_id]
            edge_strs = [f"-> {dest} (w: {weight})" for dest, weight in edges.items()]
            print(
                f"{node_obj} Connections: {', '.join(edge_strs) if edge_strs else 'None'}"
            )


@timer
def part1():
    graph, _ = parse_file("input01.txt")

    calculate_brightness(graph)

    last_node_id = max(graph.nodes.keys())
    print(f"Last plant brightness: {graph.nodes[last_node_id].energy}")


@timer
def part2():
    graph, test_cases = parse_file("input02.txt")

    sum_energies = 0
    for test_case in test_cases:
        for node_id, activate in enumerate(test_case, start=1):
            graph.add_edge(0, node_id, activate)

        calculate_brightness(graph)
        last_node_id = max(graph.nodes.keys())
        sum_energies += graph.nodes[last_node_id].energy

        for node_id in graph.nodes:
            graph.nodes[node_id].energy = 0
        graph.nodes[0].energy = 1

    print(f"Sum of plant brightness: {sum_energies}")


@timer
def part3():
    # TODO: Implement part 3
    graph, test_cases = parse_file("input_sample03.txt")


def calculate_brightness(graph: DirectedWeightedGraph):
    # Perform a topological sort

    # Calculate how many connections are comming in for each node
    in_degrees = defaultdict(int)
    for node_id in graph.nodes:
        if node_id not in in_degrees:
            in_degrees[node_id] = 0
        for neighbor in graph.get_neighbors(node_id):
            in_degrees[neighbor] += 1

    # Wnqueue nodes with indegree 0
    queue = deque([u for u in graph.nodes if in_degrees[u] == 0])

    # Store partial incoming energy for each node
    incoming_energy = [node.energy for node in graph.nodes.values()]

    while queue:
        u = queue.popleft()
        if incoming_energy[u] >= graph.nodes[u].thickness:
            graph.nodes[u].energy = incoming_energy[u]
        else:
            graph.nodes[u].energy = 0

        u_values = graph.nodes[u]
        for v in graph.adj_list.get(u, []):
            incoming_energy[v] += graph.get_weight(u, v) * u_values.energy
            in_degrees[v] -= 1
            if in_degrees[v] == 0:
                queue.append(v)


def parse_file(file_name: str) -> Tuple[DirectedWeightedGraph, List[Tuple[int]]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    graph = DirectedWeightedGraph()
    test_cases = []
    with open(abs_file_path, "r") as f:
        data = f.read().split("\n\n")

        graph.add_node(0, 1, 1)

        for plant in data:
            if not re.search(r"Plant", plant):
                for test in plant.strip().split("\n"):
                    test_cases.append(tuple(map(int, test.strip().split(" "))))
                break

            plant = plant.split("\n")
            node, branches = plant[0], plant[1:]

            matches = re.findall(r"Plant\s(\d+)\swith\sthickness\s(-?\d+):", node)
            plant_id, thickness = int(matches[0][0]), int(matches[0][1])
            graph.add_node(plant_id, thickness)

            for branch in branches:
                matches = re.findall(
                    r"-\sfree\sbranch\swith\sthickness\s(-?\d+)", branch
                )
                if len(matches) > 0:
                    graph.add_edge(0, plant_id, int(matches[0][0]))
                else:
                    matches = re.findall(
                        r"-\sbranch\sto\sPlant\s(\d+)\swith\sthickness\s(-?\d+)", branch
                    )
                    if len(matches) > 0:
                        graph.add_edge(int(matches[0][0]), plant_id, int(matches[0][1]))

    return graph, test_cases


part1()
part2()
# part3()
