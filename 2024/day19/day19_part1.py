from __future__ import annotations
from pathlib import Path
from functools import lru_cache

lines = Path("input.txt").read_text(encoding="utf-8").split("\n")
scarfs = lines[0].split(", ")
sequences = lines[2:]


@lru_cache(maxsize=None)
def solve(sequence: str):
    if not sequence:
        return True
    for chunk in scarfs:
        if chunk in sequence:
            left, right = sequence.split(chunk, 1)
            if solve(left) and solve(right):
                return True
    return False


total = 0
for sequence in sequences:
    if solve(sequence):
        print(sequence)
        total += 1
print(total)
