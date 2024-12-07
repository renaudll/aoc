from pathlib import Path
import itertools


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def concat(a, b):
    return int(str(a) + str(b))


_OPERATORS = [add, mul, concat]


def is_equation_possible(result, numbers):
    num_operators = len(numbers) - 1
    for guess_operators in itertools.product(_OPERATORS, repeat=num_operators):
        total = numbers[0]
        for operator, next_number in zip(guess_operators, numbers[1:]):
            total = operator(total, next_number)
        if total == result:
            return True
    return False


answer = 0
lines = Path("input.txt").read_text(encoding="utf-8").split("\n")
for line in lines:
    result_str, remainder = line.split(": ")
    result = int(result_str)
    numbers = [int(number) for number in remainder.split(" ")]
    if is_equation_possible(result, numbers):
        answer += result

print(answer)
