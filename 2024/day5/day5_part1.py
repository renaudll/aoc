from pathlib import Path
from collections import defaultdict

data = Path("input.txt").read_text(encoding="utf-8")

rules = defaultdict(set)
sequences = []

reading_rules = True
for line in data.split("\n"):
    if not line:
        reading_rules = False
        continue
    if reading_rules:
        before, after = line.split("|")
        before = int(before)
        after = int(after)
        rules[before].add(after)
    else:
        sequence = [int(number) for number in line.split(",")]
        sequences.append(sequence)

total = 0
for i, sequence in enumerate(sequences):
    middle_index = int(len(sequence) / 2)
    middle_value = sequence[middle_index]
    # validate
    seen = set()
    for number in sequence:
        # Check if we already encountered any number that should be after.
        if seen & rules.get(number, set()):
            break   # invalid
        seen.add(number)
    else:
        print(i, "is valid", middle_value)
        total += middle_value
print(total)
