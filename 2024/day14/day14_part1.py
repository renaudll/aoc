from pathlib import Path
import re
from dataclasses import dataclass
REGEX = re.compile(r"p=(\w+),(\w+) v=(-?\w+),(-?\w+)")
data = Path("input.txt").read_text(encoding="utf-8").split("\n")
GRID_WIDTH = 101
GRID_HEIGHT = 103
NUM_ITERATION = 100


@dataclass
class Robot:
    x: int
    y: int
    velocity_x: int
    velocity_y: int


robots = []
for line in data:
    x, y, vx, vy = (int(group) for group in REGEX.match(line).groups())
    robot = Robot(x, y, vx, vy)
    robots.append(robot)


for i in range(NUM_ITERATION):
    for robot in robots:
        robot.x = (robot.x + robot.velocity_x) % GRID_WIDTH
        robot.y = (robot.y + robot.velocity_y) % GRID_HEIGHT

quadran_tl = 0
quadran_tr = 0
quadran_bl = 0
quadran_br = 0
mid_line_vertical = (GRID_WIDTH + 1) / 2 - 1
mid_line_horizontal = (GRID_HEIGHT + 1) / 2 - 1
for robot in robots:
    if robot.x == mid_line_vertical or robot.y == mid_line_horizontal:
        continue
    if robot.x < mid_line_vertical:
        if robot.y < mid_line_horizontal:
            quadran_tl += 1
        else:
            quadran_bl += 1
    else:
        if robot.y < mid_line_horizontal:
            quadran_tr += 1
        else:
            quadran_br += 1
print(quadran_bl * quadran_br * quadran_tr * quadran_tl)

# 233709840