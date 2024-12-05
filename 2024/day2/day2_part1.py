from pathlib import Path

_THRESHOLD = 3


def read_input():
    path = Path("input.txt")
    lines = path.read_text(encoding="utf-8").split("\n")
    return [[int(token) for token in line.split(" ")] for line in lines]


def is_safe(numbers):
    current = None
    increasing = None
    for number in numbers:
        if current is None:
            current = number
            continue
        delta = abs(current - number)
        if delta < 1 or delta > _THRESHOLD:
            return False
        if number > current:
            if increasing is False:
                return False
            increasing = True
        if number < current:
            if increasing is True:
                return False
            increasing = False
        current = number
    return True

lines = read_input()

for line in lines:
    print(line, is_safe(line))

print(sum(is_safe(line)for line in lines))