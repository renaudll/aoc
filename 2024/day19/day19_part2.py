from __future__ import annotations
from pathlib import Path
from functools import lru_cache

lines = Path("input.txt").read_text(encoding="utf-8").split("\n")
scarfs = lines[0].split(", ")
sequences = lines[2:]


@lru_cache(maxsize=None)
def solve(sequence: str):
    if not sequence:
        return 1
    total = 0
    for chunk in scarfs:
        if sequence.startswith(chunk):
            right = sequence[len(chunk):]
            count = solve(right)
            if count:
                total += count
    return total


total = 0
for sequence in sequences:
    score = solve(sequence)
    total += score
print(total)
