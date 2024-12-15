import re
from dataclasses import dataclass
from pathlib import Path
from aoc_utils import Vector2D

REGEX = re.compile(r"")

MOVE_LEFT = "<"
MOVE_UP = "^"
MOVE_RIGHT = ">"
MOVE_DOWN = "v"
WALL = "#"
SPACE = "."
BOX = "O"


@dataclass
class SomeClass:
    some_property: int



grid_str, instructions_str = Path("input.txt").read_text(encoding="utf-8").split("\n\n")
grid = [[char for char in line] for line in grid_str.split("\n")]
grid_height = len(grid)
grid_width = len(grid[0])
# Find player position
for x in range(grid_width):
    for y in range(grid_height):
        cell = grid[y][x]
        if cell == "@":
            PLAYER_POS = Vector2D(x, y)
            break


def move_left():
    # Find available space
    space_position = None
    for x in range(PLAYER_POS.x, 0, -1):
        if grid[PLAYER_POS.y][x] == WALL:
            break
        if grid[PLAYER_POS.y][x] == SPACE:
            space_position = x
            break
    if space_position is None:
        return

    for x in range(space_position, PLAYER_POS.x+1):
        grid[PLAYER_POS.y][x] = grid[PLAYER_POS.y][x+1]

    grid[PLAYER_POS.y][PLAYER_POS.x] = "."
    PLAYER_POS.x -= 1


def move_right():
    # Find available space
    space_position = None
    for x in range(PLAYER_POS.x, grid_width):
        if grid[PLAYER_POS.y][x] == WALL:
            break
        if grid[PLAYER_POS.y][x] == SPACE:
            space_position = x
            break
    if space_position is None:
        return

    # Move everything before the space
    for x in reversed(range(PLAYER_POS.x, space_position+1)):
        grid[PLAYER_POS.y][x] = grid[PLAYER_POS.y][x-1]

    grid[PLAYER_POS.y][PLAYER_POS.x] = "."
    PLAYER_POS.x += 1


def move_top():
    # Find available space
    space_position = None
    for y in range(PLAYER_POS.y, 0, -1):
        if grid[y][PLAYER_POS.x] == WALL:
            break
        if grid[y][PLAYER_POS.x] == SPACE:
            space_position = y
            break
    if space_position is None:
        return

    for y in range(space_position, PLAYER_POS.y + 1):
        grid[y][PLAYER_POS.x] = grid[y+1][PLAYER_POS.x]

    grid[PLAYER_POS.y][PLAYER_POS.x] = "."
    PLAYER_POS.y -= 1


def move_bottom():
    # Find available space
    space_position = None
    for y in range(PLAYER_POS.y, grid_height):
        if grid[y][PLAYER_POS.x] == WALL:
            break
        if grid[y][PLAYER_POS.x] == SPACE:
            space_position = y
            break
    if space_position is None:
        return

    # Move everything before the space
    for y in reversed(range(PLAYER_POS.y, space_position+1)):
        grid[y][PLAYER_POS.x] = grid[y-1][PLAYER_POS.x]

    grid[PLAYER_POS.y][PLAYER_POS.x] = "."
    PLAYER_POS.y += 1

_FUNC_BY_INST = {
    MOVE_LEFT: move_left,
    MOVE_RIGHT: move_right,
    MOVE_UP: move_top,
    MOVE_DOWN: move_bottom,
}

def _debug():
    for y in range(grid_height):
        print("".join(grid[y]))

instructions = list(instructions_str)
#_debug()
for instruction in instructions:
    if instruction == "\n":
        continue
    fn = _FUNC_BY_INST[instruction]
    print(fn.__name__)
    fn()
    #_debug()

sum = 0
for x in range(grid_width):
    for y in range(grid_height):
        if grid[y][x] == BOX:
            sum += 100 * y + x
print(sum)
# Process
