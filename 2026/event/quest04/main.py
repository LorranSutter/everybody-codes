import os
import re
from dataclasses import dataclass
from collections import defaultdict

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


@dataclass(frozen=True)
class Result:
    ID: int
    quest: int
    part: int
    time: int


@timer
def part1():
    results = parse_file("input01.txt")

    checksums = defaultdict(int)
    for result in results:
        checksums[result.ID] += result.time

    checksums = sorted(checksums.values())
    total_checksum = sum(i * checksum for i, checksum in enumerate(checksums, 1))

    print(f"Total checksum: {total_checksum}")


@timer
def part2():
    results = parse_file("input02.txt")

    ranking = dict()
    for result in results:
        if result.ID not in ranking:
            ranking[result.ID] = [1, result.time]
        else:
            ranking[result.ID][0] += 1
            ranking[result.ID][1] += result.time

    ranking = sorted(ranking.values(), key=lambda item: (-item[0], item[1]))
    total_checksum = sum(i * rank[1] for i, rank in enumerate(ranking, 1))

    print(f"Total checksum: {total_checksum}")


@dataclass
class Ranking:
    time: int = 0
    points: int = 0


@timer
def part3():
    # 5151936, length correct, first character incorrect
    # TODO: Implement part 3
    all_results = parse_file("input_sample03.txt")
    part_points = [50, 100, 150]

    all_results = sorted(
        all_results, key=lambda result: (result.quest, result.part, result.time)
    )

    quests = defaultdict(list)
    for results in all_results:
        quests[results.quest].append(results)

    total_points = defaultdict(int)
    for quest_id in quests.keys():
        ranking = defaultdict(Ranking)
        print(f"Quest {quest_id}")
        for part_id, points in enumerate(part_points, 1):
            results = [r for r in quests[quest_id] if r.part == part_id]
            times = defaultdict(int)
            for result in results:
                times[result.ID] += result.time + ranking[result.ID].time

            if len(times) == 0:
                continue

            times = dict(sorted(times.items(), key=lambda item: item[1]))
            print(times)
            # ranking = dict(sorted(ranking.items(), key=lambda item: item[1].time))
            # print(ranking)

            # TODO Attribute points
            previous_time = list(times.values())[0]
            previous_points = points
            for ID in times.keys():
                # print(points)
                if times[ID] != previous_time:
                    ranking[ID].points += points
                    previous_points = points
                else:
                    ranking[ID].points += previous_points

                ranking[ID].time = times[ID]

                previous_time = ranking[ID].time
                points -= 1
                if points < 0:
                    points = 0

            print(ranking)
            print()

        for ID in ranking.keys():
            total_points[ID] += ranking[ID].points

    print(total_points)

    total_points = sorted(total_points.values(), reverse=True)
    print(total_points)
    total_checksum = 0
    previous_points = 0
    place = 1
    for points in total_points:
        total_checksum += place * points
        if points != previous_points:
            place += 1
        previous_points = points

    print(f"Total checksum: {total_checksum}")


def parse_file(file_name: str) -> list[Result]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    results = []
    with open(abs_file_path, "r") as f:
        for line in f:
            line = re.findall(
                r"id=(\d+)\squest=(\d+)\spart=(\d+)\stime=(\d+)", line.strip()
            )[0]
            ID, quest, part, time = map(int, line)
            results.append(Result(ID, quest, part, time))
    return results


part1()
part2()
part3()
