from pathlib import Path
from dataclasses import dataclass

data = Path("input.txt").read_text(encoding="utf-8")


@dataclass
class Block:
    index_number: int

# Unpack
block_index_counter = 0
unpacked = []
for index, number_str in enumerate(data):
    number = int(number_str)
    if not number:  # ignore zero
        continue
    if index % 2 == 1:  # free space:
        unpacked += ["."] * number
    else:  # number:
        for _ in range(number):
            unpacked.append(Block(index_number=block_index_counter))
        block_index_counter += 1

# Defragment
start_index = 0
end_index = len(unpacked) - 1
while start_index < end_index:
    if unpacked[start_index] != ".":  # find something to replace
        start_index += 1
        continue
    if unpacked[end_index] == ".":  # find something to replace with
        end_index -= 1
        continue
    unpacked[start_index] = unpacked[end_index]
    unpacked[end_index] = "."

total = sum(index * value.index_number for index, value in enumerate(unpacked) if value != ".")

print(total)

# 89755341581 too low
# 6291146824486