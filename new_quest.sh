#!/bin/bash

# Check if arguments are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <year> <quest>"
    echo "Example: $0 2025 1"
    exit 1
fi

# Validate inputs are numbers
if ! [[ "$1" =~ ^[0-9]+$ ]] || ! [[ "$2" =~ ^[0-9]+$ ]]; then
    echo "Error: Both year and quest must be numbers"
    exit 1
fi

year="$1"
# Format quest with leading zero (2 digits)
quest=$(printf "%02d" "$2")
folder_name="${year}/quest${quest}"

# Create year folder if it doesn't exist
if [ ! -d "$year" ]; then
    mkdir "$year"
    echo "Created folder: $year"
fi

# Check if quest folder already exists
if [ -d "$folder_name" ]; then
    echo "Error: Folder $folder_name already exists"
    exit 1
fi

# Create quest folder
mkdir "$folder_name"
echo "Created folder: $folder_name"

# Create main.py file
cat > "$folder_name/main.py" << 'EOF'
import os
from typing import Tuple

from utils.timer import timer

"""
Explanation
"""


@timer
def part1():
    # TODO: Implement part 1
    lines = parse_file("input_sample01.txt")
    pass


@timer
def part2():
    # TODO: Implement part 2
    lines = parse_file("input_sample02.txt")
    pass


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file("input_sample03.txt")
    pass


def parse_file(file_name: str) -> Tuple[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    lines = []
    with open(abs_file_path, "r") as f:
        for line in f:
            lines.append(line.strip().split())
    return lines


# part1()
# part2()
# part3()
EOF

echo "Created file: $folder_name/main.py"

# Create input01.txt file
touch "$folder_name/input01.txt"
echo "Created file: $folder_name/input01.txt"
# Create input02.txt file
touch "$folder_name/input02.txt"
echo "Created file: $folder_name/input02.txt"
# Create input03.txt file
touch "$folder_name/input03.txt"
echo "Created file: $folder_name/input03.txt"

# Create input_sample01.txt file
touch "$folder_name/input_sample01.txt"
echo "Created file: $folder_name/input_sample01.txt"
# Create input_sample02.txt file
touch "$folder_name/input_sample02.txt"
echo "Created file: $folder_name/input_sample02.txt"
# Create input_sample03.txt file
touch "$folder_name/input_sample03.txt"
echo "Created file: $folder_name/input_sample03.txt"

echo "Done!"