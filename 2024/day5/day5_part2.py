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
    valid_sequence = []

    correct = True
    # validate
    seen = set()
    for number in sequence:
        # Check if we already encountered any number that should be after.
        children = seen & rules.get(number, set())
        if children:
            correct = False
            insertion_index = min(valid_sequence.index(child) for child in children)
            valid_sequence.insert(insertion_index, number)
            print(number, children)
        else:
            valid_sequence.append(number)
        seen.add(number)
    # else:
    #     print(i, "is valid", middle_value)
    #     total += middle_value
    if not correct:
        print(sequence, valid_sequence)
        middle_index = int(len(valid_sequence) / 2)
        middle_value = valid_sequence[middle_index]
        total += middle_value

print(total)
