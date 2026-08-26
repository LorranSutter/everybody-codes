# :duck: Everybody Codes

[![Dashboard](https://img.shields.io/badge/Dashboard-coding--challenges-blue?style=for-the-badge)](https://github.com/LorranSutter/coding-challenges) <!-- BADGE:START -->[![Solved Challenges](https://img.shields.io/badge/Solved%20Challenges-70-brightgreen?style=for-the-badge&logo=python&logoColor=white)](https://everybody.codes)<!-- BADGE:END -->

This repository contains my solutions for the [Everybody Codes](https://everybody.codes) event.

Everybody Codes is an annual coding challenge that runs throughout November, featuring daily programming puzzles released Monday to Friday. Each quest challenges your problem-solving skills and algorithmic thinking.

<!-- SUMMARY:START -->
## 📊 Progress

> **Overall: 70/138 parts solved (51%)**

### [2024 — The Kingdom of Algorithmia](./2024/event/)

`████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░` **12/60** parts solved (20%)

### [2024 — Story: Echoes of Enigmatus](./2024/story01/)

`█████████` **9/9** parts solved (100%)

### [2024 — Story: The Digital Atelier](./2024/story04/)

`███░░░░░░` **3/9** parts solved (33%)

### [2025 — Event: The Song of Ducks and Dragons](./2025/event/)

`██████████████████████████████████████████████░░░░░░░░░░░░░░` **46/60** parts solved (77%)

<!-- SUMMARY:END -->

## 🛠️ Setup

### Creating a Virtual Environment

```bash
python3 -m venv .venv
```

### Activating the Virtual Environment

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

Deactivating the Virtual Environment

```bash
deactivate
```

## ✨ Creating a New Quest

To create a new quest structure, use the `new_quest.sh` script:

```bash
./new_quest.sh <year> <event|storyNN> <quest>
```

Each year has a single `event`; stories are numbered folders (`story01`, `story02`, …) matching the [everybody.codes](https://everybody.codes) story order.

Examples:
```bash
./new_quest.sh 2025 event 1
./new_quest.sh 2024 story04 1
```

This will create:
- A folder structure: `2025/event/quest01/` (or `2024/story04/quest01/`)
- `main.py` with a template for part 1, part 2 and part 3
- `input01.txt`, `input02.txt`, `input03.txt` for the quest input
- `input_sample01.txt`, `input_sample02.txt`, `input_sample03.txt` for sample/test input

## 🚀 Running Solutions

You can run the solutions:

```bash
python3 -m 2025.event.quest01.main
```

Replace `2025` with the desired year and `quest01` with the specific quest you want to run.

## 🔄 Updating Progress Summary

To update the progress summary in this README after solving new parts, run the `generate_readme.py` script:

```bash
python3 generate_readme.py
```