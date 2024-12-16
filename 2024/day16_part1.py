from __future__ import annotations
import sys
sys.setrecursionlimit(100000)

from pathlib import Path


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
        #maze_row.append(True if char == WALL else False)
        maze_row.append(char)
    maze.append(maze_row)
maze_height = len(maze)
maze_width = len(maze[0])

minimum_cost_by_coord = {}


def _iter_available_positions(x: int, y: int):
    if x > 0:
        yield x-1, y
    if x < maze_width-1:
        yield x+1, y
    if y > 0 :
        yield x, y - 1
    if y < maze_height-1:
        yield x, y + 1


def dfs(pos: tuple[int, int], direction, known=None, score=0):
    known = known or set()

    values = set()
    for child in _iter_available_positions(*pos):
        if child in known:
            continue
        known.add(child)

        cell = maze[child[1]][child[0]]
        if cell == "#":
            continue

        child_direction = (child[0] - pos[0], child[1] - pos[1])
        child_score = score + 1  # advancing
        if child_direction != direction:
            child_score += 1000  # turning

        # if child in minimum_cost_by_coord and minimum_cost_by_coord[child] < child_score:
        #     continue
        # minimum_cost_by_coord[child] = child_score

        if child == END_POSITION:
            values.add(child_score)
        else:
            values.add(dfs(child, child_direction, known=known.copy(), score=child_score))

    return min(values) if values else 99999999999999999999


print(START_POSITION)
print(dfs(START_POSITION, DIRECTION))

# 79412 is too high
