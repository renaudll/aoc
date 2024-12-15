import re
from dataclasses import dataclass
from pathlib import Path
from aoc_utils import Vector2D, dfs

REGEX = re.compile(r"")


@dataclass
class SomeClass:
    some_property: int


DATA = Path("input.txt").read_text(encoding="utf-8").split("\n")

# Parse data
for line in DATA:
    entries = REGEX.match(line).groups()

# Process
