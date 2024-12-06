from pathlib import Path

GUARD = "^"
WALL = "#"
FLOOR = "."
guard_orientation = 0  # 0 is up, 1 is right, 2 is down, 3 if left
grid = Path("input.txt").read_text(encoding="utf-8").split("\n")

# Get wall coordinates
guard_x, guard_y = None, None
grid_height = len(grid)
grid_width = len(grid[0])
wall_coordinates = set()
seen = set()
next_tile: tuple[int, int] = (0, 0)
wall_candidates = set()

# Conceptualize map
for y in range(grid_height):
    for x in range(grid_width):
        cell = grid[y][x]
        if cell == WALL:
            wall_coordinates.add((x, y))
        elif cell == GUARD:
            guard_x, guard_y = x, y

while True:
    if guard_orientation == 0:  # up
        next_x, next_y = guard_x, guard_y - 1
    elif guard_orientation == 1:  # right
        next_x, next_y = guard_x + 1, guard_y
    elif guard_orientation == 2:  # down
        next_x, next_y = guard_x, guard_y + 1
    else:  # left
        next_x, next_y = guard_x - 1, guard_y

    # Check bound
    if next_x < 0 or next_x >= grid_width or next_y < 0 or next_y >= grid_height:
        #seen.add((guard_x, guard_y))  # don't forget the last position
        break

    seen.add((guard_x, guard_y, guard_orientation))

    next_orientation_if_wall = (guard_orientation + 1) % 5
    if grid[next_y][next_x] == WALL:
        guard_orientation = next_orientation_if_wall
    else:
        # If it WAS a wall, would that result in a loop?
        if (guard_x, guard_y, next_orientation_if_wall) in seen:
            print(next_x+1, next_y+1)
            wall_candidates.add((next_x, next_y))

        guard_x, guard_y = next_x, next_y

print(len(wall_candidates))
# 227 is too low
# 228 is too low