import logging
import re
import sys
import time
from collections import ChainMap
from enum import StrEnum
from pathlib import Path

import numpy as np

test_answer = 10


class Tile(StrEnum):
    north_south = "|"
    east_west = "-"
    north_east = "L"
    north_west = "J"
    south_west = "7"
    south_east = "F"
    start = "S"
    not_pipe = "."
    inside = "I"


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

    global landscape
    landscape = np.zeros((n_lines, line_len), dtype=object)
    for idx, line in enumerate(lines):
        landscape[idx, :] = tuple(map(Tile, line))
    #  show_landscape(landscape)
    global directions
    directions = {
        "east": {
            "idx": [0, 1],
            "next": list(map(Tile, ["J", "-", "7"])),
        },
        "west": {
            "idx": [0, -1],
            "next": list(map(Tile, ["F", "-", "L"])),
        },
        "north": {
            "idx": [-1, 0],
            "next": list(map(Tile, ["F", "|", "7"])),
        },
        "south": {
            "idx": [1, 0],
            "next": list(map(Tile, ["J", "|", "L"])),
        },
    }

    two_star()


def show_landscape(landscape=None):
    for row in landscape:
        print(*[f"{str(tile):4}" for tile in row])


def one_star():
    show_landscape(landscape)
    start_idx = np.where(landscape == "S")
    start_idx = np.array([start_idx[0][0], start_idx[1][0]])

    current_idx = start_idx
    next_tiles = []
    for direction, value in directions.items():
        d_idx = value["idx"]
        next_possible = value["next"]
        next_idx = current_idx + d_idx
        if np.all(next_idx >= [0, 0]) and np.all(next_idx < [n_lines, line_len]):
            next_tile = get_tile(next_idx)
            if next_tile in next_possible:
                next_tiles.append(
                    (
                        direction,
                        next_idx,
                    )
                )

    print(next_tiles)
    current = next_tiles[0]
    n_steps = 1
    while ~np.all(start_idx == current[1]):
        n_steps += 1
        print(current)
        current = move_to_next_tile(current)

    print(n_steps / 2)


def move_to_next_tile(current):
    direction, idx = current
    d_idx = directions[direction]["idx"]
    tile = get_tile(idx)

    if tile in ["|", "-"]:
        new_direction = direction
        new_idx = idx + d_idx
    elif direction == "north":
        if tile == "F":
            new_direction = "east"
            new_idx = idx + [0, 1]
        if tile == "7":
            new_direction = "west"
            new_idx = idx + [0, -1]
    elif direction == "south":
        if tile == "L":
            new_direction = "east"
            new_idx = idx + [0, 1]
        if tile == "J":
            new_direction = "west"
            new_idx = idx + [0, -1]
    elif direction == "east":
        if tile == "7":
            new_direction = "south"
            new_idx = idx + [1, 0]
        if tile == "J":
            new_direction = "north"
            new_idx = idx + [-1, 0]
    elif direction == "west":
        if tile == "F":
            new_direction = "south"
            new_idx = idx + [1, 0]
        if tile == "L":
            new_direction = "north"
            new_idx = idx + [-1, 0]
    return (new_direction, new_idx)


def get_tile(idx):
    return landscape[*idx]


def two_star():
    show_landscape(landscape)
    start_idx = np.where(landscape == "S")
    start_idx = np.array([start_idx[0][0], start_idx[1][0]])

    current_idx = start_idx
    next_tiles = []
    for direction, value in directions.items():
        d_idx = value["idx"]
        next_possible = value["next"]
        next_idx = current_idx + d_idx
        if np.all(next_idx >= [0, 0]) and np.all(next_idx < [n_lines, line_len]):
            next_tile = get_tile(next_idx)
            if next_tile in next_possible:
                next_tiles.append(
                    (
                        direction,
                        next_idx,
                    )
                )

    current = next_tiles[0]
    d_idx = next_tiles[0][1] - next_tiles[1][1]
    possible_starting_tiles = list(
        map(
            lambda t: {x for x in Tile if t[0] in x.name},
            next_tiles,
        )
    )
    landscape[*start_idx] = (
        possible_starting_tiles[0] & possible_starting_tiles[1]
    ).pop()
    #  show_landscape(landscape)

    pipe_bool = np.zeros_like(landscape)
    pipe_bool[*start_idx] = 1
    pipe_bool[*current[1]] = 1
    pipe_i = np.zeros_like(landscape)
    pipe_i[*start_idx] = 0
    pipe_i[*current[1]] = 1

    n_steps = 1
    while ~np.all(start_idx == current[1]):
        pipe_bool[*current[1]] = 1
        pipe_i[*current[1]] = n_steps
        n_steps += 1
        #  print(current)
        current = move_to_next_tile(current)

    show_landscape(pipe_bool)
    #  show_landscape(pipe_i)

    inside = -1
    pipe_inside = np.zeros_like(landscape)
    count = 0
    for row_idx, row in enumerate(landscape):
        last_turn_pipe = None
        for column_idx, tile in enumerate(row):
            idx = (row_idx, column_idx)
            if pipe_bool[*idx]:
                if tile == "|":
                    inside *= -1
                if tile == "F" or tile == "L":
                    last_turn_pipe = tile
                if tile == "J" or tile == "7":
                    if (tile == "7" and last_turn_pipe == "L") or (
                        tile == "J" and last_turn_pipe == "F"
                    ):
                        inside *= -1
                    last_turn_pipe = None

            elif inside == 1:
                count += 1
    print(count)


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
