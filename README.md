# :duck: Everybody Codes

This repository contains my solutions for the [Everybody Codes](https://everybody.codes) event.

Everybody Codes is an annual coding challenge that runs throughout November, featuring daily programming puzzles released Monday to Friday. Each quest challenges your problem-solving skills and algorithmic thinking.

## Creating a New Quest

To create a new quest structure, use the `new_quest.sh` script:

```bash
./new_quest.sh <year> <quest>
```

Example:
```bash
./new_quest.sh 2025 1
```

This will create:
- A folder structure: `2025/quest01/`
- `main.py` with a template for part 1, part 2 and part 3
- `input01.txt`, `input02.txt`, `input03.txt` for the quest input
- `input_sample01.txt`, `input_sample02.txt`, `input_sample03.txt` for sample/test input

## Running Solutions

You can run the solutions:

```bash
python3 -m 2025.quest01.main
```

Replace `2025` with the desired year and `quest01` with the specific quest you want to run.