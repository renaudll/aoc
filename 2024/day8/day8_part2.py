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

def _is_in_bound(x, y):
    return x >= 0 and x < grid_width and y >= 0 and y < grid_height


# Compute antinodes
for _, coordinates in coordinates_by_letters.items():
    for coord_a, coord_b in itertools.combinations(coordinates, 2):
        coord_a_x, coord_a_y = coord_a
        coord_b_x, coord_b_y = coord_b
        distance = (coord_b_x - coord_a_x, coord_b_y - coord_a_y)
        distance_x, distance_y = distance

        antinodes_coordinates.add(coord_a)
        antinodes_coordinates.add(coord_b)

        antinode_coord = coord_b
        while True:
            antinode_coord = (antinode_coord[0] + distance_x, antinode_coord[1] + distance_y)
            if _is_in_bound(*antinode_coord):
                antinodes_coordinates.add(antinode_coord)
            else:
                break

        antinode_coord = coord_a
        while True:
            antinode_coord = (antinode_coord[0] - distance_x, antinode_coord[1] - distance_y)
            if _is_in_bound(*antinode_coord):
                antinodes_coordinates.add(antinode_coord)
            else:
                break

print(len(antinodes_coordinates))

