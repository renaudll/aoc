from pathlib import Path
import re

data = Path("input.txt").read_text(encoding="utf-8")
data = data.replace("\n", "")
data = re.sub(r"(don't\(\).*?do\(\))", "", data)
result = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)
total = sum(int(a) * int(b) for a, b in result)
print(total)
