# :duck: Everybody Codes

This repository contains my solutions for the [Everybody Codes](https://everybody.codes) event.

Everybody Codes is an annual coding challenge that runs throughout November, featuring daily programming puzzles released Monday to Friday. Each quest challenges your problem-solving skills and algorithmic thinking.

<!-- SUMMARY:START -->
## Progress

> **Overall: 49/54 parts solved (91%)**

### 2024 — Story

`████████████████████` **9/9** parts solved (100%)

| Quest | Part 1 | Part 2 | Part 3 |
|:------|:------:|:------:|:------:|
| Quest 01 | ⭐ | ⭐ | ⭐ |
| Quest 02 | ⭐ | ⭐ | ⭐ |
| Quest 03 | ⭐ | ⭐ | ⭐ |

### 2025 — Event

`██████████████████░░` **40/45** parts solved (89%)

| Quest | Part 1 | Part 2 | Part 3 |
|:------|:------:|:------:|:------:|
| Quest 01 | ⭐ | ⭐ | ⭐ |
| Quest 02 | ⭐ | ⭐ | ⭐ |
| Quest 03 | ⭐ | ⭐ | ⭐ |
| Quest 04 | ⭐ | ⭐ | ⭐ |
| Quest 05 | ⭐ | ⭐ | ⭐ |
| Quest 06 | ⭐ | ⭐ | ⭐ |
| Quest 07 | ⭐ | ⭐ | ⭐ |
| Quest 08 | ⭐ | ⭐ | ⬚ |
| Quest 09 | ⭐ | ⭐ | ⭐ |
| Quest 10 | ⭐ | ⬚ | ⬚ |
| Quest 11 | ⭐ | ⭐ | ⭐ |
| Quest 12 | ⭐ | ⭐ | ⭐ |
| Quest 13 | ⭐ | ⭐ | ⭐ |
| Quest 14 | ⭐ | ⭐ | ⭐ |
| Quest 15 | ⭐ | ⬚ | ⬚ |

<!-- SUMMARY:END -->


## Creating a New Quest

To create a new quest structure, use the `new_quest.sh` script:

```bash
./new_quest.sh <year> <event|story> <quest>
```

Example:
```bash
./new_quest.sh 2025 event 1
```

This will create:
- A folder structure: `2025/event/quest01/`
- `main.py` with a template for part 1, part 2 and part 3
- `input01.txt`, `input02.txt`, `input03.txt` for the quest input
- `input_sample01.txt`, `input_sample02.txt`, `input_sample03.txt` for sample/test input

## Running Solutions

You can run the solutions:

```bash
python3 -m 2025.event.quest01.main
```

Replace `2025` with the desired year and `quest01` with the specific quest you want to run.

## Updating Progress Summary

To update the progress summary in this README after solving new parts, run the `generate_readme.py` script:

```bash
python3 generate_readme.py
```