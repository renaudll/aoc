from pathlib import Path

GUARD = "^"
WALL = "#"
FLOOR = "."
ORIENTATION = 0  # 0 is up, 1 is right, 2 is down, 3 if left
grid = Path("input.txt").read_text(encoding="utf-8").split("\n")

# Get wall coordinates
guard_x, guard_y = None, None
grid_height = len(grid)
grid_width = len(grid[0])
wall_coordinates = set()
seen = set()
next_tile: tuple[int, int] = (0, 0)

# Conceptualize map
for y in range(grid_height):
    for x in range(grid_width):
        cell = grid[y][x]
        if cell == WALL:
            wall_coordinates.add((x, y))
        elif cell == GUARD:
            guard_x, guard_y = x, y

while True:
    if ORIENTATION == 0:  # up
        next_x, next_y = guard_x, guard_y - 1
    elif ORIENTATION == 1:  # right
        next_x, next_y = guard_x + 1, guard_y
    elif ORIENTATION == 2:  # down
        next_x, next_y = guard_x, guard_y + 1
    else:  # left
        next_x, next_y = guard_x - 1, guard_y

    # Check bound
    if next_x < 0 or next_x > grid_width or next_y < 0 or next_y > grid_height:
        seen.add((guard_x, guard_y))  # don't forget the last position
        break

    next_cell = grid[next_y][next_x]
    if next_cell == WALL:
        ORIENTATION = (ORIENTATION + 1) % 5
    else:
        seen.add((guard_x, guard_y))
        print(guard_x+1, guard_y+1)
        guard_x, guard_y = next_x, next_y

print(len(seen))

# too low: 4972