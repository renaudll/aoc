data = "773 79858 0 71 213357 2937 1 3998391"
data = [int(number) for number in data.split(" ")]

# If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
# If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
# If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.

print("Initial arrangement:\n" + " ".join(str(number) for number in data))
NUM_BLINKS = 25
for i in range(NUM_BLINKS):
    print(i)
    new_data = []
    for number in data:
        if not number:
            new_data.append(1)
        else:
            number_str = str(number)
            if len(number_str) % 2 == 0:
                half_len = len(number_str) // 2
                left_number_str = number_str[:half_len]
                right_number_str = number_str[half_len:]
                new_data.extend((int(left_number_str), int(right_number_str)))
            else:
                new_data.append(number * 2024)
    data = new_data
    #print("\nAfter {} blinks:\n".format(i + 1) + " ".join(str(number) for number in data))

print(len(data))

# too low: 112992
