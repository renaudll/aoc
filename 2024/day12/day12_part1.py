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

    def is_touching(self, x, y):
        return (x, y - 1) in self.coordinates

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

regions = []
previous_line_regions = []
current_line_regions = []
for y, line in enumerate(GRID):
    previous_line_regions = current_line_regions
    current_line_regions = []
    previous_letter = None
    current_cluster_coords = set()
    for x, char in enumerate(line):
        coord = (x, y)
        if previous_letter is None:
            previous_letter = char
        if char == previous_letter:
            current_cluster_coords.add(coord)

        if char != previous_letter or x == GRID_WIDTH-1:  # still reading cluster:
            # Do we need to merge it with an existing region?
            for region in previous_line_regions:
                if region.letter == previous_letter and any(region.is_touching(*coord) for coord in current_cluster_coords):
                    region.coordinates.update(current_cluster_coords)
                    break
            else:
                region = Region(previous_letter, current_cluster_coords)
                current_line_regions.append(region)
                regions.append(region)

for region in regions:
    region.compute_dimensions()
    print(region)

total = sum(region.area * region.perimeter for region in regions)

print(total)

