import logging
import re
import sys
import time
from collections import ChainMap
from pathlib import Path

import numpy as np

test_answer = 4361


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

    global times, distances
    def line_to_values(line):
        return [int(x) for x in line.split(" ")[1:]]
    times, distances = map(line_to_values, lines)

    two_star()


def one_star():
    result = list(map(race_to_ways_to_win, zip(times, distances)))
    result = np.prod(result)
    print(result)


def race_to_ways_to_win(race_spec):
    time, distance = race_spec
    distance += 1e-10
    p = np.array([-1, time, -distance])
    roots = np.roots(p)
    roots.sort()
    n_ways_to_win = int(np.floor(roots[1]) - np.ceil(roots[0]) + 1)
    return n_ways_to_win


def two_star():
    def line_to_race(line):
        numbers = line.split(" ")[1:]
        number = ''
        for sub in numbers:
            number += sub
        return int(number)
    time, distance = map(line_to_race, lines)
    print(race_to_ways_to_win((time, distance)))


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
