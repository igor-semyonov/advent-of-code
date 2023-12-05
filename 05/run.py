import logging
import re
import sys
import time
from collections import ChainMap
from pathlib import Path

import numpy as np
import scipy

test_answer = 35


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
    #  if input[-1] == "\n":
    #      input = input[:-1]
    lines = input.split("\n")[::-1]
    n_lines = len(lines)
    line_len = len(lines[0])
    #  input_array = np.array([list(line) for line in lines])

    one_star()


def one_star():
    seeds = [int(seed) for seed in lines.pop()[6:].strip().split(" ")]

    previous_items = seeds
    while True:
        try:
            line = lines.pop()
        except IndexError:
            line = "last time"

        if line == "" or line == "last time":
            try:
                map
            except UnboundLocalError:
                map = []
                continue

            next_items = []
            for item in previous_items:
                for m in map:
                    source_start = m["source_start"]
                    destination_start = m["destination_start"]
                    length = m["length"]
                    if item in range(source_start, source_start + length):
                        next_item = destination_start + item - source_start
                        break
                else:
                    next_item = item
                next_items.append(next_item)

            if line == "last time":
                break
            previous_items = next_items
            map = []
            continue
        if "-to-" in line:
            map_from, map_to = line[:-5].split("-to-")
            continue
        destination_start, source_start, length = [
            int(x) for x in line.strip().split(" ")
        ]
        map.append({
            "destination_start": destination_start,
            "source_start": source_start,
            "length": length,
        })

    print(min(next_items))


def two_star():
    pass


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
