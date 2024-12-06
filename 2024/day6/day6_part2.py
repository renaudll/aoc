import copy
from pathlib import Path

GUARD = "^"
WALL = "#"
FLOOR = "."
guard_orientation = 0  # 0 is up, 1 is right, 2 is down, 3 if left
grid = Path("input.txt").read_text(encoding="utf-8").split("\n")
grid = [list(row) for row in grid]

# Get wall coordinates
guard_x, guard_y = None, None
grid_height = len(grid)
grid_width = len(grid[0])
wall_coordinates = set()
seen = set()
next_tile = (0, 0)
wall_candidates = set()

# Conceptualize map
for y in range(grid_height):
    for x in range(grid_width):
        cell = grid[y][x]
        if cell == WALL:
            wall_coordinates.add((x, y))
        elif cell == GUARD:
            guard_x, guard_y = x, y


def _get_next_position(x, y, orientation):
    if orientation == 0:  # up
        return x, y - 1
    elif orientation == 1:  # right
        return x + 1, y
    elif orientation == 2:  # down
        return x, y + 1
    else:  # left
        return x - 1, y


def _is_out_of_bound(x, y):
    return x < 0 or x >= grid_width or y < 0 or y >= grid_height


def is_looping_if_adding_wall(x, y, orientation, wall_x, wall_y, seen):
    global grid
    grid[wall_y][wall_x] = WALL  # mutability for speed
    seen = copy.copy(seen)
    try:
        while True:
            next_x, next_y = _get_next_position(x, y, orientation)

            # Check bound
            if _is_out_of_bound(next_x, next_y):
                return False

            key = (next_x, next_y, orientation)
            if key in seen:  # if we walk on the same path, we are looping
                return True
            seen.add(key)

            if grid[next_y][next_x] == WALL:  # turn on wall
                orientation = (orientation + 1) % 4
            else:  # otherwise advance
                x, y = next_x, next_y
    finally:
        grid[wall_y][wall_x] = FLOOR


checked_wall_coordinates = set()
while True:
    next_x, next_y = _get_next_position(guard_x, guard_y, guard_orientation)

    # Exit when out of bound
    if _is_out_of_bound(next_x, next_y):
        break

    seen.add((guard_x, guard_y, guard_orientation))

    if grid[next_y][next_x] == WALL:  # turn when facing a wall
        guard_orientation = (guard_orientation + 1) % 4
    else:
        if (next_x, next_y) not in checked_wall_coordinates:
            checked_wall_coordinates.add((next_x, next_y))
            if is_looping_if_adding_wall(guard_x, guard_y, guard_orientation, next_x, next_y, seen):
                wall_candidates.add((next_x, next_y))

        guard_x, guard_y = next_x, next_y

print(len(wall_candidates))
