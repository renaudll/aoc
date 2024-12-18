from __future__ import annotations
import sys
sys.setrecursionlimit(100000)

from pathlib import Path


WALL = "#"
START = "S"
END = "E"
FLOOR = "."
START_POSITION = (0,0)
END_POSITION = (70, 70)

# Parse data
maze_width = 71
maze_height = 71
maze = [[FLOOR] * maze_width for y in range(maze_height)]
data = Path("input.txt").read_text(encoding="utf-8").split("\n")
total_num_bytes = len(data)
NUM_BYTES = 2800

for i, line in enumerate(data):
    if i == NUM_BYTES:
        break
    x, y = line.split(",")
    x = int(x)
    y = int(y)
    maze[y][x] = WALL


def debug():
    for row in maze:
        print(" ".join(row))


def _iter_available_positions(x: int, y: int):
    if x > 0:
        yield x-1, y
    if x < maze_width-1:
        yield x+1, y
    if y > 0 :
        yield x, y - 1
    if y < maze_height-1:
        yield x, y + 1


score_map = {}


def dfs(pos: tuple[int, int],  score=0):
    values = set()
    for child in _iter_available_positions(*pos):
        cell = maze[child[1]][child[0]]
        if cell == "#":
            continue

        child_score = score + 1  # advancing

        if child in score_map and score_map[child] <= child_score:
            continue
        score_map[child] = child_score

        if child == END_POSITION:
            values.add(child_score)
        else:
            values.add(dfs(child, score=child_score))

    return min(values) if values else 99999999999999999999


print(dfs(START_POSITION))


for i in range(NUM_BYTES, total_num_bytes):
    print(i)
    line = data[i]
    x, y = line.split(",")
    x = int(x)
    y = int(y)
    maze[y][x] = WALL
    score_map.clear()
    if dfs(START_POSITION) == 99999999999999999999:
        print(f"{x},{y}")
        break

# 446 is right
