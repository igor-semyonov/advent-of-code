import copy
import logging
import re
import sys
import time
from collections import ChainMap
from pathlib import Path

import numpy as np

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

    two_star()


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
        map.append(
            {
                "destination_start": destination_start,
                "source_start": source_start,
                "length": length,
            }
        )

    print(min(next_items))


def two_star():
    seeds_line = [int(seed) for seed in lines.pop()[6:].strip().split(" ")]

    seeds = []
    for value, length in np.array(seeds_line).reshape((len(seeds_line) // 2, 2)):
        seeds.append(
            [
                value,
                length,
            ]
        )

    previous_items = seeds
    lines.pop()  # get rid of first blank line

    i = -1
    map = []
    next_items = []
    while True:
        try:
            line = lines.pop()
        except IndexError:
            line = "last time"
        i += 1

        if line == "" or line == "last time":
            next_items += previous_items
            previous_items = next_items
            if line == "last time":
                break
            continue

        if "-to-" in line:
            map_from, map_to = line[:-5].split("-to-")
            next_items = []
            continue

        destination_start, source_start, map_length = [
            int(x) for x in line.strip().split(" ")
        ]

        tmp_items = previous_items
        previous_items = []
        while True:
            try:
                start, length = tmp_items.pop()
            except IndexError:
                break

            if (start + length <= source_start) or (start >= source_start + map_length):
                previous_items.append([start, length])
            elif start >= source_start:
                if start + length <= source_start + map_length:
                    next_items.append(
                        [destination_start + start - source_start, length]
                    )
                else:
                    next_items.append(
                        [
                            destination_start + start - source_start,
                            map_length - start + source_start,
                        ]
                    )
                    tmp_items.append(
                        [
                            source_start + map_length,
                            length - (source_start + map_length - start),
                        ]
                    )
            elif start < source_start:
                if start + length <= source_start + map_length:
                    next_items.append(
                        [destination_start, start - source_start + length]
                    )
                    tmp_items.append([start, source_start - start])
                else:
                    next_items.append([destination_start, map_length])
                    tmp_items.append([start, source_start - start])
                    tmp_items.append(
                        [
                            source_start + map_length,
                            length - (source_start - start + map_length),
                        ]
                    )
            else:
                previous_items.append([start, length])

    print(np.array(next_items)[:, 0].min())


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
