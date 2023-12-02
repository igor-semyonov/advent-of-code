import re
import time
from pathlib import Path

number_to_int = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "enin": 9,
    "thgie": 8,
    "neves": 7,
    "xis": 6,
    "evif": 5,
    "ruof": 4,
    "eerht": 3,
    "owt": 2,
    "eno": 1,
    "orez": 0,
}


def main():
    input_file = Path("./input")
    lines = input_file.read_text().split("\n")
    #  if len(lines[-1]) == 0:
    #      lines = lines[:-8]

    #  idx = 0
    #  line = lines[idx]
    #  print(line, line_to_value_2(line))

    result = sum(map(line_to_value_2, lines))
    print(result)


def line_to_value_2(line):
    total = 0
    try:
        first_digit = re.search(
            r"0|1|2|3|4|5|6|7|8|9|zero|one|two|three|four|five|six|seven|eight|nine",
            line.casefold(),
        ).group()
    except AttributeError:
        return 0

    last_digit = re.search(
        r"0|1|2|3|4|5|6|7|8|9|eroz|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin",
        line[::-1].casefold(),
    ).group()

    try:
        total += 10 * int(first_digit)
    except ValueError:
        total += 10 * number_to_int[first_digit]

    try:
        total += int(last_digit)
    except ValueError:
        total += number_to_int[last_digit]

    return total


def line_to_value(line):
    total = 0
    for c in line:
        if c in "0123456789":
            total += 10 * int(c)
            break

    for c in line[::-1]:
        if c in "0123456789":
            total += int(c)
            break
    return total


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
