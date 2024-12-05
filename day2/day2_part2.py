from pathlib import Path

_THRESHOLD = 3


def read_input():
    path = Path("input.txt")
    lines = path.read_text(encoding="utf-8").split("\n")
    return [[int(token) for token in line.split(" ")] for line in lines]


def is_safe(numbers, index_to_skip=None):
    current = None
    increasing = None
    for index, number in enumerate(numbers):
        if index == index_to_skip:
            continue
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


def is_safe_with_fallback(numbers):
    if is_safe(numbers):
        return True
    for index in range(len(numbers)):
        if is_safe(numbers, index_to_skip=index):
            return True
    return False


lines = read_input()
print(sum(is_safe_with_fallback(line) for line in lines))
