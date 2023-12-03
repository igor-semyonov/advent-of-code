import re
import time
from collections import ChainMap
from pathlib import Path
import sys

import numpy as np
import scipy

test_answer = 4361


def main(test_file):
    one_star(test_file)


def one_star():
    global input, input_array, lines, line_len, n_lines
    print("Test file = " + test_file)
    input = Path(test_file).read_text()
    if input[-1] == "\n":
        input = input[:-1]
    lines = input.split("\n")
    n_lines = len(lines)
    line_len = len(lines[0])
    input_array = np.array([list(line) for line in lines])

    line_idx = 0
    line = lines[line_idx]
    #  part_ids = dict(ChainMap(*map(line_to_part_ids, enumerate(lines))))
    #  answer = sum(part_ids.keys())
    #  for line_idx, line in enumerate(lines):
    #      if len(line) != line_len:
    #          print(f"line {line_idx} not of same length as line 0")
    #  print(answer)
    total = sum(map(line_to_part_ids, enumerate(lines)))
    print(total)


def line_to_part_ids(line_spec: tuple):
    total = 0
    line_idx, line = line_spec
    matches = re.finditer(r"[\d]+", line)
    part_ids = {}
    for match in matches:
        part_id = int(match.group())
        start_idx = match.start()
        end_idx = match.end()
        symbol_str = ""
        #  if line_idx > 0:
        #      symbol_str += lines[line_idx - 1][start_idx:end_idx]
        #      if start_idx > 0:
        #          symbol_str += lines[line_idx - 1][start_idx - 1]
        #      if end_idx < line_len - 1:
        #          symbol_str += lines[line_idx - 1][end_idx]
        #  if line_idx < n_lines - 1:
        #      symbol_str += lines[line_idx + 1][start_idx:end_idx]
        #      if start_idx > 0:
        #          symbol_str += lines[line_idx + 1][start_idx - 1]
        #      if end_idx < line_len - 1:
        #          symbol_str += lines[line_idx + 1][end_idx]
        #  if start_idx > 0:
        #      symbol_str += lines[line_idx][start_idx - 1]
        #  if end_idx < line_len - 1:
        #      symbol_str += lines[line_idx][end_idx]

        match_array = np.zeros_like(input_array, dtype=int)
        match_array[line_idx, start_idx:end_idx] = 1
        convolution_kernel = np.ones((3, 3), dtype=int)
        neighborhood = scipy.signal.convolve2d(
            match_array, convolution_kernel, mode="same"
        )
        neighborhood = (neighborhood > 0) & ~match_array.astype(bool)
        symbol_str = "".join(input_array[neighborhood])

        symbol_str_re = re.search(r"[^.\d]", symbol_str)
        print(f'\npart location: line_idx: {line_idx}\tstart idx: {start_idx}\tend_idx: {end_idx}')
        print("neiborhood bool array: \n", neighborhood)
        print("array of neighborhood characters: ", input_array[neighborhood])
        print('part id: ', part_id, '\nsymbol string: ', symbol_str)
        print(
            'original input near this part:',
            *lines[max(line_idx - 1, 0) : min(line_idx + 2, n_lines)],
            sep="\n",
        )
        print('symbol string regex match object: ', symbol_str_re)
        if symbol_str_re is None:
            continue

        part_ids[part_id] = {
            "start_idx": start_idx,
            "end_idx": end_idx,
            "line_idx": line_idx,
        }
        total += part_id
    return total
    return part_ids


if __name__ == "__main__":
    start_time = time.perf_counter()
    if len(sys.argv) <= 1:
        print("No test file provided, using default: test-input.txt")
        test_file = "./test-input.txt"
    else:
        test_file = sys.argv[1]
    main(test_file)
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
