import re
import sys
import time
from collections import ChainMap
from pathlib import Path

import numpy as np
import scipy

test_answer = 4361


def main():
    global input_file, input, input_array, lines, line_len, n_lines
    if len(sys.argv) < 2:
        input_file = Path("./test-input.txt")
    else:
        input_file = Path(sys.argv[1])

    input = input_file.read_text()
    if input[-1] == "\n":
        input = input[:-1]
    lines = input.split("\n")
    n_lines = len(lines)
    line_len = len(lines[0])
    input_array = np.array([list(line) for line in lines])

    one_star()


def one_star():
    pass


def two_star():
    pass


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")