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
    current_cluster_letter = None
    current_cluster_coords = set()
    for x in range(GRID_WIDTH+1):  # last iteration is to flush the last cluster
        coord = (x, y)

        # Get char
        if x < GRID_WIDTH:
            char = line[x]

            if current_cluster_letter is None:
                current_cluster_letter = char
        else:
            char = None  # will force the cluster to end

        # Add char to cluster if applicable
        is_new_letter = char != current_cluster_letter
        if not is_new_letter:
            current_cluster_coords.add(coord)
        # Push cluster when it end
        if is_new_letter:  # still reading cluster:
            # Do we need to merge it with an existing region?
            for region in previous_line_regions:
                if region.letter == current_cluster_letter and any(region.is_touching(*coord) for coord in current_cluster_coords):
                    region.coordinates.update(current_cluster_coords)
                    break
            else:
                region = Region(current_cluster_letter, current_cluster_coords)
                regions.append(region)
            current_line_regions.append(region)
            current_cluster_coords = {coord}

        current_cluster_letter = char

for region in regions:
    region.compute_dimensions()
    print(region)

total = sum(region.area * region.perimeter for region in regions)

print(total)

# 1133206 is too low