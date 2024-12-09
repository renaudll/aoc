from pathlib import Path
from collections import defaultdict
import itertools

data = Path("input.txt").read_text(encoding="utf-8")
grid = data.split("\n")
grid_height = len(grid)
grid_width = len(grid[0])

coordinates_by_letters = defaultdict(set)

# Get antennas
for x in range(grid_width):
    for y in range(grid_height):
        cell = grid[y][x]
        if cell == ".":
            continue
        coordinates_by_letters[cell].add((x, y))

antinodes_coordinates = set()

# Compute antinodes
for _, coordinates in coordinates_by_letters.items():
    for coord_a, coord_b in itertools.combinations(coordinates, 2):
        coord_a_x, coord_a_y = coord_a
        coord_b_x, coord_b_y = coord_b
        distance = (coord_b_x - coord_a_x, coord_b_y - coord_a_y)
        distance_x, distance_y = distance
        antinode_coord_1 = (coord_b_x + distance_x, coord_b_y + distance_y)
        antinode_coord_2 = (coord_a_x - distance_x, coord_a_y - distance_y)
        for antinode_coord in (antinode_coord_1, antinode_coord_2):
            x, y = antinode_coord
            if x >= 0 and x < grid_width and y >= 0 and y < grid_height:
                antinodes_coordinates.add(antinode_coord)

print(len(antinodes_coordinates))