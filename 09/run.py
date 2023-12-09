import logging
import re
import sys
import time
from collections import ChainMap
from pathlib import Path

import numpy as np

test_answer = 114


def main():
    logging.basicConfig(level=logging.INFO)

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

    two_star()


def one_star():
    sequences = [*map(line_to_sequences, lines)]
    print(sum(
        map(
            lambda x: x[0][-1],
            sequences
        )
    ))


def line_to_sequences(line):
    sequences = [np.array([*map(int, line.split(" "))])]

    while True:
        sequences.append(sequence_difference(sequences[-1]))
        if np.all(sequences[-1] == 0):
            break

    for idx in range(len(sequences)-1, -1, -1):
        sequence = sequences[idx]
        sequence = np.append(
            sequence,
            sequence[-1] + (sequences[idx + 1][-1] if idx < len(sequences) - 1 else 0),
        )
        sequences[idx] = sequence
    return sequences


def sequence_difference(sequence):
    return sequence[1:] - sequence[:-1]


def two_star():
    sequences = [*map(line_to_sequences_2, lines)]
    print(sum(
        map(
            lambda x: x[0][0],
            sequences
        )
    ))


def line_to_sequences_2(line):
    sequences = [np.array([*map(int, line.split(" "))])]

    while True:
        sequences.append(sequence_difference(sequences[-1]))
        if np.all(sequences[-1] == 0):
            break

    for idx in range(len(sequences)-1, -1, -1):
        sequence = sequences[idx]
        sequence = np.insert(
            sequence,
            0,
            sequence[0] - (sequences[idx + 1][0] if idx < len(sequences) - 1 else 0),
        )
        sequences[idx] = sequence
    return sequences


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
