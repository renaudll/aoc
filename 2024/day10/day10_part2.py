import copy
from pathlib import Path
from collections import defaultdict

grid = Path("input.txt").read_text(encoding="utf-8").split("\n")
grid_height = len(grid)
grid_width = len(grid[0])

start_coords = []

for y in range(grid_height):
    for x in range(grid_width):
        cell = grid[y][x]
        if cell == "0":
            start_coords.append((x, y))

ends_by_start = defaultdict(list)


def explore_path(start, current, x, y, known=None, path=None):
    known = known or set()
    known = copy.copy(known) or set()
    path = copy.copy(path) or []

    coord = (x, y)
    if coord in known:
        return
    known.add(coord)

    if grid[y][x] == ".":
        return
    cell = int(grid[y][x])

    if current is not None and cell - current != 1:  # only consider increases by 1
        return

    path.append(coord)

    if cell == 9:
        global ends_by_start
        ends_by_start[start].append(coord)
        print(path)
        return

    if x > 0:
        explore_path(start, cell, x-1, y, known=known, path=path)
    if x < grid_width - 1:
        explore_path(start, cell, x+1, y, known=known, path=path)
    if y > 0:
        explore_path(start, cell, x, y-1, known=known, path=path)
    if y < grid_height - 1:
        explore_path(start, cell, x, y+1, known=known, path=path)


for coord in start_coords:
    explore_path(coord, None, coord[0], coord[1])

total = 0
for start, ends in ends_by_start.items():
    total += len(ends)
#total = sum(ends_by_start.values())
print(total)