from pathlib import Path
import re

def read_input():
    path = Path("input.txt")
    return path.read_text(encoding="utf-8")

data = read_input()
regex = r"mul\((\d+),(\d+)\)"

result = re.findall(regex, data)
total = 0
for a, b in result:
    total += int(a) * int(b)
print(total)
