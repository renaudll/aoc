import functools

DATA = "773 79858 0 71 213357 2937 1 3998391"
NUMBERS = [int(number) for number in DATA.split(" ")]
NUM_BLINKS = 75


@functools.lru_cache(maxsize=None)
def solve(iteration_count, number):
    number_str = str(number)
    is_even_digits = len(number_str) % 2 == 0

    # We can easily compute one iteration
    if iteration_count == 1:
        return 2 if is_even_digits else 1

    # Solve recursively
    if number == 0:
        return solve(iteration_count - 1, 1)
    elif is_even_digits:
        half_len = len(number_str) // 2
        left_number = int(number_str[:half_len])
        right_number = int(number_str[half_len:])
        return solve(iteration_count - 1, left_number) + solve(iteration_count - 1, right_number)
    else:
        return solve(iteration_count - 1, number * 2024)


total = sum(solve(NUM_BLINKS, number) for number in NUMBERS)
print(total)
