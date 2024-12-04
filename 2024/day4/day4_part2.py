from pathlib import Path

word = "MAS"
word_reversed = word[::-1]
word_len = len(word)

data = Path("input.txt").read_text(encoding="utf-8").split("\n")
width = len(data[0])
height = len(data)

def check(row, col):
    line1 = data[row-1][col-1] + data[row][col] + data[row+1][col+1]
    line2 = data[row+1][col-1] + data[row][col] + data[row-1][col+1]
    return line1 in (word, word_reversed) and line2 in (word, word_reversed)


total = 0
for row in range(1, height-1):
    for col in range(1, width-1):
        if check(row, col):
            total += 1
print(total)
