import logging
import re
import sys
import time
from collections import ChainMap
from pathlib import Path

import numpy as np

test_answer = 405


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

    mirrors = []
    while True:
        try:
            idx = lines.index("")
            mirror = np.array([*map(lambda x: list(x), lines[: idx - 1])])
        except ValueError:
            idx = 0
            mirror = np.array([*map(lambda x: list(x), lines)])
            idx = 0
        mirrors.append(mirror)
        lines = lines[idx + 1 :]
        if idx == 0:
            break
    #  print(*[mirror.shape for mirror in mirrors])

    idx = 0
    mirror = mirrors[idx]

    row_locations = sum(
        map(
            find_mirror,
            mirrors,
        )
    )
    col_locations = sum(
        map(
            find_mirror,
            [mirror.T for mirror in mirrors],
        )
    )

    print(100 * row_locations + col_locations)


def find_mirror(mirror):
    n_rows, _ = mirror.shape
    row_comparison = np.zeros((n_rows, n_rows), dtype=np.int8)
    for row0_idx, row0 in enumerate(mirror):
        for row1_idx, row1 in enumerate(mirror):
            row_match = np.all(row0 == row1)
            row_comparison[row0_idx, row1_idx] = row_match
    row_comparison = np.flip(row_comparison, 1)
    print(row_comparison)
    for idx in range(1, n_rows-1):
        diagonal = np.diagonal(row_comparison, -idx)
        print(diagonal)
        if np.all(diagonal):
            mirror_row = (n_rows + idx) // 2
            print(mirror_row)
            return mirror_row
    return 0


def one_star():
    pass


def two_star():
    pass


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
