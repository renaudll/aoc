from __future__ import annotations
from pathlib import Path
from collections import deque


WALL = "#"
START = "S"
END = "E"
FLOOR = "."
START_POSITION = None
END_POSITION = None
DIRECTION = (1, 0)

# Parse data
maze = []
data = Path("input.txt").read_text(encoding="utf-8").split("\n")
for y, line in enumerate(data):
    maze_row = []
    for x, char in enumerate(line):
        if char == START:
            START_POSITION = (x, y)
            char = "."
        elif char == END:
            END_POSITION = (x, y)
            char = "."
        maze_row.append(char)
    maze.append(maze_row)
maze_height = len(maze)
maze_width = len(maze[0])


cost_map: dict[tuple[int, int], int | None] = {(x, y): None for x in range(maze_width) for y in range(maze_height)}


def solve():
    doit = deque([(START_POSITION, (1, 0), 0)])
    while doit:
        coord, direction, score = doit.pop()
        x, y = coord

        # Ignore if highest
        known_cost = cost_map[coord]
        if known_cost and known_cost < score:
            continue
        cost_map[coord] = score

        for child in ((x, y+1), (x-1, y), (x+1, y),  (x, y-1)):
            if maze[child[1]][child[0]] != FLOOR:
                continue
            child_direction = (child[0] - coord[0], child[1] - coord[1])
            child_score = score + 1  # advancing
            if direction != child_direction:
                child_score += 1000

            doit.append((child, child_direction, child_score))


solve()
print(cost_map[END_POSITION])
