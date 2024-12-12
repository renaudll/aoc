from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass
GRID = Path("input.txt").read_text(encoding="utf-8").split("\n")
GRID_HEIGHT = len(GRID)
GRID_WIDTH = len(GRID[0])


@dataclass
class Region:
    letter: str
    coordinates: set[tuple[int, int]]
    area: int = 0
    perimeter: int = 0
    num_sides: int = 0

    def compute_dimensions(self):
        self.area = len(self.coordinates)

        perimeter = 0
        for (x, y) in self.coordinates:
            if (x-1, y) not in self.coordinates:
                perimeter += 1
            if (x+1, y) not in self.coordinates:
                perimeter += 1
            if (x, y+1) not in self.coordinates:
                perimeter += 1
            if (x, y-1) not in self.coordinates:
                perimeter += 1
        self.perimeter = perimeter

        coords_x = {x for x, _ in self.coordinates}
        coords_y = {y for _, y in self.coordinates}
        self.num_sides = 0

        # scan side horizontally
        for y in coords_y:
            was_top_edge = False
            was_bottom_edge = False
            for x in range(GRID_WIDTH):
                is_top_edge = (x, y) in self.coordinates and (x, y-1) not in self.coordinates
                is_bottom_edge = (x, y) in self.coordinates and (x, y+1) not in self.coordinates
                if is_top_edge and not was_top_edge:  # entering
                    self.num_sides += 1
                if is_bottom_edge and not was_bottom_edge:  # existing
                    self.num_sides += 1
                was_top_edge = is_top_edge
                was_bottom_edge = is_bottom_edge
        # scan side vertically
        for x in coords_x:
            was_left_edge = False
            was_right_edge = False
            for y in range(GRID_HEIGHT):
                is_left_edge = (x, y) in self.coordinates and (x-1, y) not in self.coordinates
                is_right_edge = (x, y) in self.coordinates and (x+1, y) not in self.coordinates
                if is_left_edge and not was_left_edge:  # when entering
                    self.num_sides += 1
                if is_right_edge and not was_right_edge:  # when exiting
                    self.num_sides += 1
                was_left_edge = is_left_edge
                was_right_edge = is_right_edge



unexplored = {(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}
region_by_coord = {}
regions = []
priority = set()

while unexplored:
    if priority:
        x, y = priority.pop()
        unexplored.remove((x, y))
    else:
        x, y = unexplored.pop()
    letter = GRID[y][x]

    left_coord = (x-1, y) if x > 0 else None
    right_coord = (x+1, y) if x < GRID_WIDTH-1 else None
    top_coord = (x, y-1) if y > 0 else None
    bottom_coord = (x, y+1) if y < GRID_HEIGHT-1 else None
    left_letter = GRID[y][x-1] if left_coord else None
    right_letter = GRID[y][x+1] if right_coord else None
    top_letter = GRID[y-1][x] if top_coord else None
    bottom_letter = GRID[y+1][x] if bottom_coord else None

    candidates = []
    if left_letter == letter:
        candidates.append(left_coord)
    if right_letter == letter:
        candidates.append(right_coord)
    if top_letter == letter:
        candidates.append(top_coord)
    if bottom_letter == letter:
        candidates.append(bottom_coord)

    region = None
    for candidate in candidates:
        candidate_region = region_by_coord.get(candidate)
        if candidate_region:
            region = candidate_region
        if candidate in unexplored:
            priority.add(candidate)

    if region:
        region.coordinates.add((x, y))
    else:
        region = Region(letter, {(x, y)})
        regions.append(region)
    region_by_coord[(x, y)] = region

for region in regions:
    region.compute_dimensions()
    print(region)

total = sum(region.area * region.num_sides for region in regions)
print(total)
