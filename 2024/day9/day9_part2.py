from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass

data = Path("input.txt").read_text(encoding="utf-8")

free_space_size_by_coord = {}
block_coord_by_block_number = {}
block_by_block_number = {}

@dataclass
class Block:
    index_number: int
    size: int


# Unpack
block_index_counter = 0
unpacked = []
real_index = 0
for index, number_str in enumerate(data):
    size = int(number_str)
    if not size:  # ignore zero
        continue
    if index % 2 == 1:  # free space:
        free_space_size_by_coord[real_index] = size
        unpacked += ["."] * size
    else:  # number:
        inst = Block(index_number=block_index_counter, size=size)
        for _ in range(size):
            unpacked.append(inst)
        block_coord_by_block_number[block_index_counter] = real_index
        block_by_block_number[block_index_counter] = inst
        block_index_counter += 1
    real_index += size


# Defragment
#print("".join(str(val.index_number) if isinstance(val, Block) else val for val in unpacked))
for block_number in range(block_index_counter - 1, 0 - 1, -1):
    block = block_by_block_number[block_number]
    src_coord = block_coord_by_block_number[block_number]

    # Hack:  Remove free space that started after the original block position
    free_space_size_by_coord = {
        coord: size
        for coord, size in free_space_size_by_coord.items()
        if coord < src_coord
    }

    # Find free space
    found = False
    free_space_coords = sorted(free_space_size_by_coord)  # TODO: Always have sorted?
    for free_space_coord in free_space_coords:
        free_space_size = free_space_size_by_coord[free_space_coord]
        if free_space_size >= block.size:
            break
    else:
        continue
    free_space_size_by_coord.pop(free_space_coord)  # unregister
    dst_coord = free_space_coord

    # Move block
    for i in range(block.size):
        unpacked[dst_coord + i] = block
        unpacked[src_coord + i] = "."

    # Adjust free space after moving
    if free_space_size != block.size:  # register smaller free space
        free_space_size_by_coord[dst_coord + block.size] = free_space_size - block.size

    #print("".join(str(val.index_number) if isinstance(val, Block) else val for val in unpacked))

total = sum(index * value.index_number for index, value in enumerate(unpacked) if value != ".")

print(total)

# 11526264308139 is too high
# 9961575911745  is too high
# 6307280105216 is too high
# 6307280105216 is too high
# 6307279963620