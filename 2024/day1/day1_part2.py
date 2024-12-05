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

count_by_number = {}
for number in list2:
    if number in count_by_number:
        count_by_number[number] += 1
    else:
        count_by_number[number] = 1
total = 0
for a in list1:
    total += a * count_by_number.get(a, 0)
print(total)