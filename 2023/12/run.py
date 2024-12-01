import logging
import re
import sys
import time
from collections import ChainMap
from pathlib import Path

import numpy as np

test_answer = [1, 4, 1, 1, 4, 10]


def main():
    global input_file, input, input_array, lines, line_len, n_lines
    if len(sys.argv) < 2:
        input_file = Path("./test-input.txt")
    else:
        input_file = Path(sys.argv[1])

    input = re.sub(
        " +",
        " ",
        input_file.read_text(),
    ).strip()
    lines = input.split("\n")
    n_lines = len(lines)
    line_len = len(lines[0])
    #  input_array = np.array([list(line) for line in lines])

    line_idx = 2
    line = lines[line_idx]
    #  for line in lines:
    springs, records = line.split(" ")
    #  springs = springs.strip(".")
    #  springs = re.sub("[.]+", ".", springs)
    records = [int(r) for r in records.split(",")]
    bs = broken_springs(springs, records)
    print(bs)

    bs = [*map(line_to_bs, lines)]
    print(bs)
    print(sum(bs))


def line_to_bs(line):
    springs, records = line.split(" ")
    records = [int(r) for r in records.split(",")]
    return broken_springs(springs, records)


def broken_springs(springs, records):
    print(springs, records)
    if len(records) == 1:
        if records[0] == len(springs):
            if springs.find(".") == -1:
                return 1
    if len(records) == 0:
        if springs.find("#") == -1:
            return 1
    if len(springs) == 0:
        if len(records) == 0:
            return 1
        return 0
    elif len(records) == 0:
        return 0

    len_springs = len(springs.strip("."))
    record = records[0]
    remaining_records = records[1:]

    re_string = f"[?#]{{{record}}}"
    regex = re.compile(re_string)
    matches = myfindall(regex, springs)
    if record == 3:
        print(matches)
    count = 0
    for match in matches:
        try:
            if match.start() > 0:
                if springs[match.start() - 1] == "#":
                    continue
            if springs[match.end()] == "#":
                continue
        except IndexError:
            pass
        remaining_springs = springs[match.end() + 1 :]
        print(match)
        count += broken_springs(
            remaining_springs,
            remaining_records,
        )
    return count


def myfindall(regex, seq):
    matches = []
    pos = 0

    while True:
        match = regex.search(seq, pos)
        if match is None:
            break
        matches.append(match)
        pos = match.start() + 1
    return matches


def one_star():
    pass


def two_star():
    pass


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
