import copy
import logging
import re
import sys
import time
from collections import ChainMap
from pathlib import Path

import numpy as np

test_answer = 4361


def main():
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

    universe = np.array([list(line) for line in lines])
    #  universe = expand_universe(universe)
    blank_rows, blank_columns = expand_universe(universe)
    expansion_factor = 1_000_000

    galaxies = np.array(np.where(universe == "#")).T
    path_sum = 0
    paths = []
    for g0_idx, g0 in enumerate(galaxies[:-1]):
        for g1 in galaxies[g0_idx+1:]:
            path = np.sum(np.abs(g0 - g1))
            for idx in blank_rows:
                if idx > min(g0[0], g1[0]) and idx < max(g0[0], g1[0]):
                    path += expansion_factor - 1
            for idx in blank_columns:
                if idx > min(g0[1], g1[1]) and idx < max(g0[1], g1[1]):
                    path += expansion_factor - 1
            paths.append([g0, g1, path, g0-g1])
            path_sum += path

    print(path_sum)
    one_star()


def expand_universe(universe):
    blank_rows = []
    blank_columns = []
    for idx, row in enumerate(universe):
        if "#" not in row:
            blank_rows.append(idx)
    for idx, col in enumerate(universe.T):
        if "#" not in col:
            blank_columns.append(idx)
    return blank_rows, blank_columns


def one_star():
    pass


def two_star():
    pass


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
