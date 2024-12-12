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


unexplored = {(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}
region_by_coord = {}
regions = []

while unexplored:
    x, y = unexplored.pop()
    letter = GRID[y][x]

    # Find region to merge with
    left_region = region_by_coord.get((x-1, y)) if x > 0 else None
    right_region = region_by_coord.get((x+1, y)) if x < GRID_WIDTH-1 else None
    top_region = region_by_coord.get((x, y-1)) if y > 0 else None
    bottom_region = region_by_coord.get((x, y+1)) if y < GRID_HEIGHT-1 else None
    region = next(
        (
            candidate
            for candidate in (left_region, right_region, top_region, bottom_region)
            if candidate and candidate.letter == letter
        ),
        None
    )
    if region:
        region.coordinates.add((x, y))
    else:
        region = Region(letter, {(x, y)})
        regions.append(region)
    region_by_coord[(x, y)] = region

for region in regions:
    region.compute_dimensions()
    print(region)

total = sum(region.area * region.perimeter for region in regions)

print(total)
