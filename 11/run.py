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
    universe = expand_universe(universe)

    galaxies = np.array(np.where(universe == "#")).T
    path_sum = 0
    paths = []
    for g0_idx, g0 in enumerate(galaxies[:-1]):
        for g1 in galaxies[g0_idx+1:]:
            path = np.sum(np.abs(g0 - g1))
            paths.append([g0, g1, path, g0-g1])
            path_sum += path

    print(path_sum)
    one_star()


def expand_universe(universe):
    n_rows, n_cols = universe.shape
    new_universe = np.copy(universe)
    for idx, row in enumerate(universe[::-1, :]):
        row_idx = n_rows - idx - 1
        if "#" not in row:
            #  print(f"found empty row at {row_idx}")
            new_universe = np.insert(
                new_universe,
                row_idx,
                ".",
                axis=0,
            )
    for idx, col in enumerate(universe.T[::-1, :]):
        col_idx = n_cols - idx - 1
        if "#" not in col:
            #  print(f"found empty column at {col_idx}")
            new_universe = np.insert(
                new_universe,
                col_idx,
                ".",
                axis=1,
            )
    return new_universe


def one_star():
    pass


def two_star():
    pass


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
