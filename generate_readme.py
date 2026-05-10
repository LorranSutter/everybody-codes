#!/usr/bin/env python3
"""
Scans all quest folders and generates a progress summary in README.md.

For each quest's main.py, it checks whether part1(), part2(), part3() contain
a "# TODO" comment in the first line of the function body. If so, the part is
considered unsolved.

The summary is injected between <!-- SUMMARY:START --> and <!-- SUMMARY:END -->
markers in README.md, preserving all other content.
"""

import os
import re
from pathlib import Path


ROOT = Path(__file__).parent


def find_quests(root: Path) -> dict:
    """
    Returns a nested dict: {year: {type: {quest_number: {part: solved}}}}
    """
    results = {}

    for year_dir in sorted(root.iterdir()):
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue
        year = year_dir.name

        for type_dir in sorted(year_dir.iterdir()):
            if not type_dir.is_dir() or type_dir.name.startswith("."):
                continue
            quest_type = type_dir.name

            for quest_dir in sorted(type_dir.iterdir()):
                if not quest_dir.is_dir():
                    continue
                match = re.match(r"quest(\d+)", quest_dir.name)
                if not match:
                    continue

                quest_num = int(match.group(1))
                main_file = quest_dir / "main.py"
                if not main_file.exists():
                    continue

                parts = check_parts(main_file)
                results.setdefault(year, {}).setdefault(quest_type, {})[quest_num] = parts

    return results


def check_parts(main_file: Path) -> dict:
    """
    Parses main.py and checks if part1/part2/part3 functions have a # TODO
    in the first non-empty line of the function body.
    Returns {1: True/False, 2: True/False, 3: True/False} where True = solved.
    """
    content = main_file.read_text()
    parts = {}

    for part_num in [1, 2, 3]:
        pattern = rf"def part{part_num}\(.*?\):\s*\n(.*?)(?=\ndef |\Z)"
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            parts[part_num] = False
            continue

        body = match.group(1)
        first_code_line = ""
        for line in body.split("\n"):
            stripped = line.strip()
            if stripped:
                first_code_line = stripped
                break

        parts[part_num] = "# TODO" not in first_code_line

    return parts


def generate_summary(results: dict) -> str:
    """Generates the markdown summary from scan results."""
    lines = []
    lines.append("## Progress")
    lines.append("")

    total_solved = 0
    total_parts = 0

    for year in sorted(results.keys()):
        for quest_type in sorted(results[year].keys()):
            quests = results[year][quest_type]
            type_label = quest_type.capitalize()

            solved = sum(
                1 for q in quests.values() for p, s in q.items() if s
            )
            total = sum(len(q) for q in quests.values())
            total_solved += solved
            total_parts += total

            pct = (solved / total * 100) if total > 0 else 0
            filled = round(pct / 5)
            bar = "█" * filled + "░" * (20 - filled)

            lines.append(f"### {year} — {type_label}")
            lines.append("")
            lines.append(f"`{bar}` **{solved}/{total}** parts solved ({pct:.0f}%)")
            lines.append("")
            lines.append("| Quest | Part 1 | Part 2 | Part 3 |")
            lines.append("|:------|:------:|:------:|:------:|")

            for quest_num in sorted(quests.keys()):
                parts = quests[quest_num]
                cols = []
                for p in [1, 2, 3]:
                    cols.append("⭐" if parts.get(p, False) else "⬚")
                lines.append(
                    f"| Quest {quest_num:02d} | {cols[0]} | {cols[1]} | {cols[2]} |"
                )

            lines.append("")

    # Overall summary
    overall_pct = (total_solved / total_parts * 100) if total_parts > 0 else 0
    lines.insert(2, f"> **Overall: {total_solved}/{total_parts} parts solved ({overall_pct:.0f}%)**")
    lines.insert(3, "")

    return "\n".join(lines)


def update_readme(root: Path, summary: str) -> None:
    """
    Injects the summary between <!-- SUMMARY:START --> and <!-- SUMMARY:END -->
    markers in README.md. Adds the markers + summary at the end of the header
    section if they don't exist yet.
    """
    readme_path = root / "README.md"
    content = readme_path.read_text()

    start_marker = "<!-- SUMMARY:START -->"
    end_marker = "<!-- SUMMARY:END -->"

    block = f"{start_marker}\n{summary}\n{end_marker}"

    if start_marker in content and end_marker in content:
        # Replace existing summary
        pattern = re.compile(
            re.escape(start_marker) + r".*?" + re.escape(end_marker),
            re.DOTALL,
        )
        new_content = pattern.sub(block, content)
    else:
        # Insert after the first paragraph (after the repo description)
        # Find the end of the intro paragraph
        intro_pattern = re.compile(
            r"(# .+\n\n.+\n\n.+\n)"
        )
        match = intro_pattern.match(content)
        if match:
            insert_pos = match.end()
            new_content = (
                content[:insert_pos] + "\n" + block + "\n\n" + content[insert_pos:]
            )
        else:
            # Fallback: append at the end
            new_content = content + "\n\n" + block + "\n"

    readme_path.write_text(new_content)
    print(f"✅ README.md updated with progress summary")


def main():
    results = find_quests(ROOT)
    summary = generate_summary(results)
    update_readme(ROOT, summary)


if __name__ == "__main__":
    main()
