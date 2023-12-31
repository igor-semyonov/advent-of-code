import re
import sys
import time
from collections import ChainMap
from pathlib import Path

import numpy as np
import scipy

test_answer = 4361


def main():
    global input_file
    if len(sys.argv) < 2:
        input_file = Path("./input.txt")
    else:
        input_file = Path(sys.argv[1])

    two_star()


def two_star():
    global input, input_array, lines, line_len, n_lines
    input = input_file.read_text()
    if input[-1] == "\n":
        input = input[:-1]
    lines = input.split("\n")
    n_lines = len(lines)
    line_len = len(lines[0])
    input_array = np.array([list(line) for line in lines])

    #  line_idx = 8
    #  line = lines[line_idx]
    #  print(find_gears((line_idx, line)))

    answer = sum(map(find_gears, enumerate(lines)))
    print(answer)


def find_gears(line_spec: tuple):
    total = 0
    line_idx, line = line_spec
    potential_gears = re.finditer(r"\*", line)

    for potential_gear in potential_gears:
        ratios = []
        start_idx = potential_gear.start()
        end_idx = potential_gear.end()

        if start_idx > 0:
            match = re.search(r"^[\d]+", line[start_idx - 1 :: -1])
            if match is not None:
                ratios.append(int(match.group()[::-1]))
        if end_idx < line_len - 1:
            match = re.search(r"^[\d]+", line[end_idx:])
            if match is not None:
                ratios.append(int(match.group()))

        other_lines = []
        if line_idx > 0:
            other_lines.append(lines[line_idx - 1])
        if line_idx < n_lines - 1:
            other_lines.append(lines[line_idx + 1])
        for other_line in other_lines:
            for match in re.finditer(r"\d+", other_line):
                span = match.span()
                span = range(span[0] - 1, span[1] + 1)
                if start_idx in span:
                    ratios.append(int(match.group()))

        if len(ratios) == 2:
            total += ratios[0] * ratios[1]
    return total


def one_star():
    global input, input_array, lines, line_len, n_lines
    input = input_file.read_text()
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
        print(
            f"\npart location: line_idx: {line_idx}\tstart idx: {start_idx}\tend_idx: {end_idx}"
        )
        print("neiborhood bool array: \n", neighborhood)
        print("array of neighborhood characters: ", input_array[neighborhood])
        print("part id: ", part_id, "\nsymbol string: ", symbol_str)
        print(
            "original input near this part:",
            *lines[max(line_idx - 1, 0) : min(line_idx + 2, n_lines)],
            sep="\n",
        )
        print("symbol string regex match object: ", symbol_str_re)
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
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
