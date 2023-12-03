import re
import time
from collections import ChainMap
from pathlib import Path

import numpy as np

test_answer = 4361


def main():
    one_star()


def two_star():
    lines = Path("./input.txt").read_text().split("\n")

    answer = sum(map(line_to_power, lines))
    print(answer)

    #  total = 0
    #  for line in lines:
    #      total += line_to_power(line)
    #  print(total)

    #  print(sum([line_to_power(line) for line in lines]))


def line_to_power(line):
    try:
        (game, handfuls) = line.split(":")
    except ValueError:
        return 0

    handfuls = handfuls.split(";")
    return np.max(list(map(handful_to_balls, handfuls)), axis=0).prod()


def one_star():
    global input, input_array, lines, line_len, n_lines
    input = Path("./input.txt").read_text()
    if input[-1] == "\n":
        input = input[:-1]
    lines = input.split("\n")
    n_lines = len(lines)
    line_len = len(lines[0])
    input_array = np.array([list(line) for line in lines])

    line_idx = 0
    line = lines[line_idx]
    part_ids = dict(ChainMap(*map(line_to_part_ids, enumerate(lines))))
    answer = sum(part_ids.keys())
    print(answer)


def line_to_part_ids(line_spec: tuple):
    line_idx, line = line_spec
    matches = re.finditer(r"[\d]+", line)
    part_ids = {}
    for match in matches:
        part_id = int(match.group())
        start_idx = match.start()
        end_idx = match.end()
        symbol_str = ""
        if line_idx > 0:
            symbol_str += lines[line_idx - 1][start_idx:end_idx]
            if start_idx > 0:
                symbol_str += lines[line_idx - 1][start_idx - 1]
            if end_idx < line_len - 1:
                symbol_str += lines[line_idx - 1][end_idx]
        if line_idx < n_lines - 1:
            symbol_str += lines[line_idx + 1][start_idx:end_idx]
            if start_idx > 0:
                symbol_str += lines[line_idx + 1][start_idx - 1]
            if end_idx < line_len - 1:
                symbol_str += lines[line_idx + 1][end_idx]
        if start_idx > 0:
            symbol_str += lines[line_idx][start_idx - 1]
        if end_idx < line_len - 1:
            symbol_str += lines[line_idx][end_idx]
        symbol_str_re = re.search(r"[^.]", symbol_str)
        print(part_id, symbol_str)
        print(
            *lines[max(line_idx - 1, 0) : min(line_idx + 2, n_lines)],
            sep="\n",
        )
        print(symbol_str_re)
        if symbol_str_re is None:
            continue

        part_ids[part_id] = {
            "start_idx": start_idx,
            "end_idx": end_idx,
            "line_idx": line_idx,
        }
    return part_ids


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
