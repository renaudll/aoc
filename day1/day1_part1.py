from pathlib import Path

lines = Path("input.txt").read_text().split("\n")
list1 = []
list2 = []
for line in lines:
    print(line)
    a, b = line.split("  ")
    a = int(a)
    b = int(b)
    list1.append(a)
    list2.append(b)
list1 = sorted(list1)
list2 = sorted(list2)

total = 0
for a, b in zip(list1, list2):
    total += abs(a - b)
print(total)