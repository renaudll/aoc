import re
from pathlib import Path

data = Path("input.txt").read_text(encoding="utf-8")
regex = r"mul\((\d+),(\d+)\)"
result = re.findall(regex, data)
total = sum(int(a) * int(b) for a, b in result)
print(total)
