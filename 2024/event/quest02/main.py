import os
from typing import Set, Tuple

from utils.timer import timer
from utils.utils import tcolors

"""
Part 1:
- First part is a bit of a cheat: I took advantage of Python's built-in string method
  `count` to count how many runes are found in the inscription.

Part 2:
- Now it gets interesting. For the second challenge of the event I wasn't expecting to
  need a Trie already, so maybe there's an easier way to do this — but this is where I
  landed.
- My main reason for using a Trie was to solve the problem of overlapping runes. I wrote
  a special function in the Trie class, similar to a traditional prefix search, except
  that instead of stopping at the first match, it keeps going and looks for the latest
  possible occurrence of a word.
  For example:
    If the word is ABCDE, and the possible runes are ABC and ABCD, a traditional prefix
    search would stop at ABC. But if we did that here, we'd miss the letter D in the
    final count, so the function keeps going and stops at ABCD instead.
  This function also returns the index of the last letter of the word found along the
  Trie path.
- Another trick here is that we add the runes to the Trie reversed as well, so we don't
  have to scan the inscriptions from right to left separately.
- Another thing that avoids double-counting overlapping runes is keeping a set that
  tracks every id that belongs to a scale. When `starts_with_rune` returns true, we know
  the id it returned is the last one of the found rune, so we add the whole range of
  valid ids from i to idx.
- One last thing that saved a step here was not splitting the inscriptions by line.
  Instead of reading a list of inscriptions, we read a single long inscription with `\n`
  between what were supposed to be separate lines, like `ABC\nDEF`. The `\n` just acts
  like a blank space and doesn't interfere with the rune search.

Part 3:
- The heavy lifting was done in part 2, so this part was mostly a matter of adjusting
  things.
- Here we can't take advantage of reading everything as a single big inscription, because
  we have to account for the loop wrapping around. To handle the wraparound, we take each
  horizontal inscription and copy its beginning onto its end — we only need to copy as
  many characters as the longest rune, since that's the worst case.
- This causes a bit of trouble when searching for runes, because if a rune is found in
  the overlap, the id range returned will fall outside the valid ids of that inscription.
  For example:
    We have an inscription ABCDEFG, with max rune size 3, so the looped version becomes
    ABCDEFGABC. If we find a rune GAB, it returns the id range from 6 to 8, but ids 8 and
    beyond don't really exist in the original inscription.
  The fix is simply to take `id % width` when adding ids to the scales set, where width
  is the known width of each horizontal inscription.
- For the vertical inscriptions, it's pretty much the same as part 2 — we build a string
  for each vertical inscription and run the same scale-counting process on it.
- The other new problem here is that a horizontal and a vertical rune can intersect. If we
  don't account for that, we'd double-count the scales where they overlap.
- The fix for this was to make the scales set a set of (x, y) coordinates instead of
  single ids.
"""


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True

    def starts_with_rune(self, word: str) -> bool:
        current = self.root
        last_id = -1
        for i, char in enumerate(word):
            if current.is_end_of_word:
                last_id = i - 1
            if char not in current.children:
                if last_id >= 0:
                    return True, last_id
                return False, i
            current = current.children[char]

        if current.is_end_of_word:
            return True, i
        elif last_id >= 0:
            return True, last_id
        return False, i


@timer
def part1():
    runes, inscription = parse_file("input01.txt")

    total_runes = sum(inscription.count(rune) for rune in runes)
    print(f"Total runes: {total_runes}")


@timer
def part2():
    runes, inscription = parse_file("input02.txt")

    trie = Trie()
    for rune in runes:
        trie.insert(rune)
        trie.insert(rune[::-1])

    max_rune_size = max([len(rune) for rune in runes])
    scales = set()
    for i in range(len(inscription)):
        truthy, idx = trie.starts_with_rune(inscription[i : i + max_rune_size])
        if truthy:
            scales.update(range(i, i + idx + 1))

    print(f"Total scales: {len(scales)}")


@timer
def part3():
    runes, inscriptions = parse_file("input03.txt")
    max_rune_size = max([len(rune) for rune in runes])

    inscriptions_h = inscriptions.split("\n")
    width = len(inscriptions_h[0])
    height = len(inscriptions_h)

    for i in range(height):
        # Maximum possible loop depends on the longest rune
        inscriptions_h[i] += inscriptions_h[i][:max_rune_size]

    inscriptions_v = [[] for _ in range(width)]
    for i in range(width):
        inscriptions_v[i] = "".join(
            (inscriptions[i + j * (width + 1)] for j in range(height))
        )

    trie = Trie()
    for rune in runes:
        trie.insert(rune)
        trie.insert(rune[::-1])

    # Keep track of (x,y)
    scales = set()
    for y, inscription in enumerate(inscriptions_h):
        for x in range(len(inscription)):
            truthy, idx = trie.starts_with_rune(inscription[x : x + max_rune_size])
            if truthy:
                for i in range(x, x + idx + 1):
                    # i % width to avoid double count when loop
                    scales.add((y, i % width))

    for x, inscription in enumerate(inscriptions_v):
        for y in range(len(inscription)):
            truthy, idx = trie.starts_with_rune(inscription[y : y + max_rune_size])
            if truthy:
                for i in range(y, y + idx + 1):
                    scales.add((i, x))

    print(f"Total scales: {len(scales)}")


def print_inscription(inscription: str, s: Set):
    output = ""
    for i in range(len(inscription)):
        if i in s:
            output += f"{tcolors.GREEN}{inscription[i]}{tcolors.RESET}"
        else:
            output += inscription[i]
    print(output, s)


def parse_file(file_name: str) -> Tuple[Tuple[str], str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    runes = []
    inscription = ""
    with open(abs_file_path, "r") as f:
        f = f.read().split("\n\n")
        runes = f[0].strip().split(":")[1].split(",")
        inscription = f[1].strip()
    return runes, inscription


part1()
part2()
part3()
