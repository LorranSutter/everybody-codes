#!/usr/bin/env python3
"""
Scans all quest folders and generates progress summaries:
- Root README.md: overall stats + progress bars per year/type (with titles)
- year/type/README.md: detailed quest tables with stars

For each quest's main.py, it checks whether part1(), part2(), part3() contain
a "# TODO" comment in the first line of the function body. If so, the part is
considered unsolved.

The root summary is injected between <!-- SUMMARY:START --> and <!-- SUMMARY:END -->
markers in README.md, preserving all other content.

Each year/type/README.md is managed between <!-- SUMMARY:START --> and
<!-- SUMMARY:END --> markers as well, so any content outside the markers
(like the title) is preserved after the first run.
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


def read_type_title(root: Path, year: str, quest_type: str) -> str:
    """
    Reads the H1 title from year/type/README.md.
    Falls back to 'year — Type' if the file doesn't exist or has no H1.
    """
    type_label = quest_type.capitalize()
    fallback = f"{year} — {type_label}"
    readme_path = root / year / quest_type / "README.md"

    if not readme_path.exists():
        return fallback

    for line in readme_path.read_text().splitlines():
        if line.startswith("# "):
            return line[2:].strip()

    return fallback


def generate_root_summary(root: Path, results: dict) -> str:
    """Generates the root README summary with progress bars only (no tables)."""
    lines = []
    lines.append("## Progress")
    lines.append("")

    total_solved = 0
    total_parts = 0

    section_lines = []

    for year in sorted(results.keys()):
        for quest_type in sorted(results[year].keys()):
            quests = results[year][quest_type]
            title = read_type_title(root, year, quest_type)

            solved = sum(
                1 for q in quests.values() for p, s in q.items() if s
            )
            total = sum(len(q) for q in quests.values())
            total_solved += solved
            total_parts += total

            pct = (solved / total * 100) if total > 0 else 0
            filled = round(pct / 5)
            bar = "█" * filled + "░" * (20 - filled)

            section_lines.append(f"### [{title}](./{year}/{quest_type}/)")
            section_lines.append("")
            section_lines.append(f"`{bar}` **{solved}/{total}** parts solved ({pct:.0f}%)")
            section_lines.append("")

    # Overall summary
    overall_pct = (total_solved / total_parts * 100) if total_parts > 0 else 0
    lines.append(f"> **Overall: {total_solved}/{total_parts} parts solved ({overall_pct:.0f}%)**")
    lines.append("")
    lines.extend(section_lines)

    return "\n".join(lines)


def generate_type_readme(year: str, quest_type: str, quests: dict) -> str:
    """Generates the quest table for a year/type README."""
    type_label = quest_type.capitalize()

    solved = sum(1 for q in quests.values() for p, s in q.items() if s)
    total = sum(len(q) for q in quests.values())
    pct = (solved / total * 100) if total > 0 else 0
    filled = round(pct / 5)
    bar = "█" * filled + "░" * (20 - filled)

    lines = []
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
            f"| [Quest {quest_num:02d}](./quest{quest_num:02d}/) | {cols[0]} | {cols[1]} | {cols[2]} |"
        )

    lines.append("")
    return "\n".join(lines)


def inject_between_markers(content: str, summary: str, default_header: str) -> str:
    """
    Replaces content between <!-- SUMMARY:START --> and <!-- SUMMARY:END --> markers.
    If markers don't exist, creates the file with a header + markers.
    """
    start_marker = "<!-- SUMMARY:START -->"
    end_marker = "<!-- SUMMARY:END -->"
    block = f"{start_marker}\n{summary}\n{end_marker}"

    if start_marker in content and end_marker in content:
        pattern = re.compile(
            re.escape(start_marker) + r".*?" + re.escape(end_marker),
            re.DOTALL,
        )
        return pattern.sub(block, content)
    else:
        # No markers yet — create with default header
        return f"{default_header}\n\n{block}\n"


def update_root_readme(root: Path, summary: str) -> None:
    """Injects the summary into the root README.md between markers."""
    readme_path = root / "README.md"
    content = readme_path.read_text()

    start_marker = "<!-- SUMMARY:START -->"
    end_marker = "<!-- SUMMARY:END -->"
    block = f"{start_marker}\n{summary}\n{end_marker}"

    if start_marker in content and end_marker in content:
        pattern = re.compile(
            re.escape(start_marker) + r".*?" + re.escape(end_marker),
            re.DOTALL,
        )
        new_content = pattern.sub(block, content)
    else:
        # Insert after the intro paragraph
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
            new_content = content + "\n\n" + block + "\n"

    readme_path.write_text(new_content)
    print(f"✅ Updated {readme_path}")


def update_type_readme(root: Path, year: str, quest_type: str, table_summary: str) -> None:
    """Creates or updates the year/type/README.md with the quest table."""
    type_label = quest_type.capitalize()
    readme_path = root / year / quest_type / "README.md"
    default_header = f"# {year} — {type_label}"

    if readme_path.exists():
        content = readme_path.read_text()
    else:
        content = ""

    new_content = inject_between_markers(content, table_summary, default_header)
    readme_path.write_text(new_content)
    print(f"✅ Updated {readme_path}")


def main():
    results = find_quests(ROOT)

    # Generate and update root README
    root_summary = generate_root_summary(ROOT, results)
    update_root_readme(ROOT, root_summary)

    # Generate and update each year/type README
    for year in sorted(results.keys()):
        for quest_type in sorted(results[year].keys()):
            quests = results[year][quest_type]
            table_summary = generate_type_readme(year, quest_type, quests)
            update_type_readme(ROOT, year, quest_type, table_summary)


if __name__ == "__main__":
    main()
