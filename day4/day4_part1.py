from pathlib import Path

word = "XMAS"
word_reversed = word[::-1]
word_len = len(word)

data = Path("input.txt").read_text(encoding="utf-8").split("\n")
width = len(data[0])
height = len(data)


def _iter_upper_edge():
    for col in range(width):
        yield 0, col

def _iter_left_edge():
    for row in range(height):
        yield row, 0

def _iter_right_edge():
    for row in range(height):
        yield row, width - 1

def _iter_bottom():
    for col in range(width):
        yield height - 1, col

def scan_vertical(column):
    return "".join(data[row][column] for row in range(height))

def scan_diagonal_forward(row, col):
    # scan upward right
    buffer = []
    while row < height and col < width:
        buffer.append(data[row][col])
        row += 1
        col += 1
    if len(buffer) >= word_len:
        return "".join(buffer)
    return None

def scan_diagonal_backward(row, col):
    # scan downright left
    buffer = []
    while row >= 0 and col >= 0:
        buffer.append(data[row][col])
        row -= 1
        col -= 1
    if len(buffer) >= word_len:
        return "".join(buffer)
    return None


to_scan = []

# Add horizontal
to_scan.extend(data)

# Add vertical
for column in range(width):
    to_scan.append(scan_vertical(column))

# Add diagonal 1
seen = set()
coords = tuple(_iter_left_edge()) + tuple(_iter_upper_edge())
for row, col in coords:
    cur = (row, col)
    if cur in seen:
        continue
    seen.add(cur)
    result = scan_diagonal_forward(row, col)
    if result:
        to_scan.append(result)

seen = set()
coords = tuple(_iter_right_edge()) + tuple(_iter_bottom())
for row, col in coords:
    cur = (row, col)
    if cur in seen:
        continue
    seen.add(cur)
    result = scan_diagonal_backward(row, col)
    if result:
        to_scan.append(result)

def count_in_line(line):
    total = 0
    window_start = 0
    window_end = word_len
    line_length = len(line)
    while window_end < line_length:
        if line[window_start:window_end] in (word, word_reversed):
            total += 1
        window_start += 1
        window_end += 1
    return total

total = 0
for i, line in enumerate(to_scan):
    line_count = count_in_line(line)
    print(line, line_count)
    total += line_count
print(total)
