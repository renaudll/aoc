import re
import itertools
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


grid_str, instructions_str = Path("input.txt").read_text(encoding="utf-8").split("\n\n")
grid = []
for line_str in grid_str.split("\n"):
    line = []
    for char in line_str:
        char1 = char
        char2 = char
        if char == "@":
            char2 = "."
        elif char == BOX:
            char1 = "["
            char2 = "]"
        line.append(char1)
        line.append(char2)
        #line.append(char)
    grid.append(line)
#grid = [[char for char in line] for line in grid_str.split("\n")]
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


def _find_space_y_upward(start_x, start_y):
    for y in range(start_y, 0, -1):
        if grid[y][start_x] == WALL:
            break
        if grid[y][start_x] == SPACE:
            return y
    return None


def _find_space_y_downward(start_x, start_y):
    for y in range(start_y, grid_height):
        if grid[y][start_x] == WALL:
            break
        if grid[y][start_x] == SPACE:
            return y
    return None

def move_coords_up(coords: list[Vector2D]):
    coords = sorted(coords, key=lambda coord: coord.y)
    for coord in coords:
        grid[coord.y][coord.x] = grid[coord.y+1][coord.x]

    # Reset highest y coords
    for coord in coords:
        if Vector2D(coord.x, coord.y+1) not in coords:
            grid[coord.y][coord.x] = "."


def move_coords_down(coords: list[Vector2D]):
    coords = sorted(coords, key=lambda coord: -coord.y)
    for coord in coords:
        grid[coord.y][coord.x] = grid[coord.y - 1][coord.x]

    # Reset highest y coords
    for coord in coords:
        if Vector2D(coord.x, coord.y-1) not in coords:
            grid[coord.y][coord.x] = "."


def move_top():
    # Find available space
    space_position = _find_space_y_upward(PLAYER_POS.x, PLAYER_POS.y)
    if not space_position:
        return

    coords_to_move = [Vector2D(PLAYER_POS.x, y) for y in range(space_position, PLAYER_POS.y + 1)]

    # Handle wide boxes
    while True:
        found_more = False
        for coord in tuple(coords_to_move):
            if grid[coord.y][coord.x] == "[":
                next_coord = Vector2D(coord.x + 1, coord.y)
                if next_coord not in coords_to_move:
                    found_more = True
                    next_space_y = _find_space_y_upward(next_coord.x, next_coord.y)
                    if not next_space_y:
                        return
                    coords_to_move.extend([Vector2D(next_coord.x, y) for y in range(next_space_y, next_coord.y + 1)])
            if grid[coord.y][coord.x] == "]":
                next_coord = Vector2D(coord.x - 1, coord.y)
                if next_coord not in coords_to_move:
                    found_more = True
                    next_space_y = _find_space_y_upward(next_coord.x, next_coord.y)
                    if not next_space_y:
                        return
                    coords_to_move.extend([Vector2D(next_coord.x, y) for y in range(next_space_y, next_coord.y + 1)])
        if not found_more:
            break

    move_coords_up(coords_to_move)

    PLAYER_POS.y -= 1


def move_bottom():
    space_position = _find_space_y_downward(PLAYER_POS.x, PLAYER_POS.y)
    if space_position is None:
        return

    # Move everything before the space
    coords_to_move = [Vector2D(PLAYER_POS.x, y) for y in range(PLAYER_POS.y, space_position+1)]

    # Handle wide boxes
    while True:
        found_more = False
        for coord in tuple(coords_to_move):
            if grid[coord.y][coord.x] == "[":
                next_coord = Vector2D(coord.x + 1, coord.y)
                if next_coord not in coords_to_move:
                    found_more = True
                    next_space_y = _find_space_y_downward(next_coord.x, next_coord.y)
                    if not next_space_y:
                        return
                    coords_to_move.extend([Vector2D(next_coord.x, y) for y in range(next_coord.y, next_space_y + 1)])
            if grid[coord.y][coord.x] == "]":
                next_coord = Vector2D(coord.x - 1, coord.y)
                if next_coord not in coords_to_move:
                    found_more = True
                    next_space_y = _find_space_y_downward(next_coord.x, next_coord.y)
                    if not next_space_y:
                        return
                    coords_to_move.extend([Vector2D(next_coord.x, y) for y in range(next_coord.y, next_space_y + 1)])
        if not found_more:
            break

    move_coords_down(coords_to_move)

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

def _validate():
    for y in range(grid_height):
        for x1, x2 in itertools.pairwise(range(grid_width)):
            cell1 = grid[y][x1]
            cell2 = grid[y][x2]
            if cell1 == "[" and cell2 != "]":
                raise ValueError(f"Invalid cell at {x1} {y}")

instructions = list(instructions_str)
for instruction in instructions:
    if instruction == "\n":
        continue
    fn = _FUNC_BY_INST[instruction]
    need_debug = instruction == MOVE_UP and grid[PLAYER_POS.y - 1][PLAYER_POS.x] != "."
    if need_debug:
        print("!!!", fn.__name__)
        _debug()
    fn()
    if need_debug:
        _debug()
        _validate()
        print()

sum = 0
for x in range(grid_width):
    for y in range(grid_height):
        if grid[y][x] == "[":
            sum += 100 * y + x
print(sum)


# 1399656 is too high
# 1397393