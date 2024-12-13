from pathlib import Path
from dataclasses import dataclass
import re

_REGEX_BUTTON = re.compile(r".*: X\+(\d+), Y\+(\d+)")
_REGEX_PRIZE = re.compile(r"Prize: X=(\d+), Y=(\d+)")
"""
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400
"""

BUTTON_A_COST = 3
BUTTON_B_COST = 1


@dataclass
class Button:
    cost: int
    offset_x: int
    offset_y: int


def _find_lowest_score(button_a: Button, button_b: Button, prize: tuple[int, int]):
    lowest_score = 0
    desired_x, desired_y = prize
    for num_button_a in range(0, 100):
        for num_button_b in range(0, 100):
            x = button_a.offset_x * num_button_a + button_b.offset_x * num_button_b
            y = button_a.offset_y * num_button_a + button_b.offset_y * num_button_b
            if x == desired_x and y == desired_y:
                cost = button_a.cost * num_button_a + button_b.cost * num_button_b
                if lowest_score == 0 or cost < lowest_score:
                    lowest_score = cost
    return lowest_score

total = 0
sections = Path("input.txt").read_text(encoding="utf-8").split("\n\n")
for section in sections:
    button_a_line, button_b_line, prize_line = section.split("\n")
    button_a_x, button_a_y = _REGEX_BUTTON.match(button_a_line).groups()
    button_b_x, button_b_y = _REGEX_BUTTON.match(button_b_line).groups()
    prize_x, prize_y = _REGEX_PRIZE.match(prize_line).groups()
    button_a = Button(BUTTON_A_COST, int(button_a_x), int(button_a_y))
    button_b = Button(BUTTON_B_COST, int(button_b_x), int(button_b_y))
    prize_coord = (int(prize_x), int(prize_y))
    print(button_a, button_b, prize_coord)
    lowest_score = _find_lowest_score(button_a, button_b, prize_coord)
    if lowest_score:
        total += lowest_score
print(total)
