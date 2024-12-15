from pathlib import Path
import re
from dataclasses import dataclass
REGEX = re.compile(r"p=(\w+),(\w+) v=(-?\w+),(-?\w+)")
data = Path("input.txt").read_text(encoding="utf-8").split("\n")
GRID_WIDTH = 101
GRID_HEIGHT = 103
NUM_ITERATION = 1000000

from PIL import Image

def create_black_white_image(bool_table, output_path):
    """
    Create a black-and-white PNG image based on a 2D table of booleans.

    Args:
        bool_table (list[list[bool]]): 2D list where True -> white pixel, False -> black pixel.
        output_path (str): File path to save the PNG image.
    """
    # Get dimensions of the table
    height = len(bool_table)
    width = len(bool_table[0]) if height > 0 else 0

    # Create a new grayscale image (mode 'L')
    image = Image.new('L', (width, height), color=0)

    # Fill the image with pixel data based on bool_table
    for y in range(height):
        for x in range(width):
            pixel_value = 255 if bool_table[y][x] else 0  # White (255) or Black (0)
            image.putpixel((x, y), pixel_value)

    # Save the image
    image.save(output_path)
    print(f"Image saved to {output_path}")
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

mid_line_vertical = (GRID_WIDTH + 1) / 2 - 1

known_state = set()
for i in range(NUM_ITERATION):
    for robot in robots:
        robot.x = (robot.x + robot.velocity_x) % GRID_WIDTH
        robot.y = (robot.y + robot.velocity_y) % GRID_HEIGHT

    count_by_line = [0] * GRID_HEIGHT
    known_pos = set()
    for robot in robots:
        count_by_line[robot.y] += 1
        known_pos.add((robot.x, robot.y))
    if tuple(sorted(known_pos)) in known_state:
        raise ValueError(i)
    known_state.add(tuple(sorted(known_pos)))

    grid = [[False] * GRID_WIDTH for line in range(GRID_HEIGHT)]
    for robot in robots:
        grid[robot.y][robot.x] = True
    create_black_white_image(grid, f"{i}.png")
