import logging
import re
import sys
import time
from collections import ChainMap
from itertools import cycle
from math import gcd
from pathlib import Path

import numpy as np

test_answer = 6


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

    global instructions, graph, starting_nodes
    instructions_list = lines[0]
    instruction_to_number = {"L": 0, "R": 1}
    instructions = cycle(map(lambda x: instruction_to_number[x], instructions_list))

    graph_lines = lines[2:]
    graph = {}
    for node_spec in graph_lines:
        node, node_to = node_spec.split(" = ")
        node_l, node_r = node_to[1:-1].split(", ")
        graph[node] = (node_l, node_r)

    starting_nodes = []
    for node in graph.keys():
        if node[-1] == "A":
            starting_nodes.append(node)

    counter_example()


def one_star():
    instructions = lines[0]
    instruction_to_number = {"L": 0, "R": 1}
    instructions = cycle(map(lambda x: instruction_to_number[x], instructions))

    graph_lines = lines[2:]
    graph = {}
    for node_spec in graph_lines:
        node, node_to = node_spec.split(" = ")
        node_l, node_r = node_to[1:-1].split(", ")
        graph[node] = (node_l, node_r)

    current_node = "AAA"
    steps = 0
    while True:
        steps += 1
        current_node = graph[current_node][next(instructions)]
        if current_node == "ZZZ":
            break
    print(steps)


def two_star():
    instructions_list = lines[0]
    instruction_to_number = {"L": 0, "R": 1}
    instructions = cycle(map(lambda x: instruction_to_number[x], instructions_list))

    graph_lines = lines[2:]
    graph = {}
    for node_spec in graph_lines:
        node, node_to = node_spec.split(" = ")
        node_l, node_r = node_to[1:-1].split(", ")
        graph[node] = (node_l, node_r)

    starting_nodes = []
    for node in graph.keys():
        if node[-1] == "A":
            starting_nodes.append(node)
    #  print(starting_nodes)

    all_steps = []
    for starting_node in starting_nodes:
        steps = 0
        instructions = cycle(map(lambda x: instruction_to_number[x], instructions_list))
        current_node = starting_node
        while True:
            steps += 1
            instruction = next(instructions)
            current_node = graph[current_node][instruction]

            if current_node[-1] == "Z":
                break
        all_steps.append(steps)

    lcm = 1
    for i in all_steps:
        lcm = lcm * i // gcd(lcm, i)
    #  print(all_steps)
    #  print(lcm)
    return lcm


def counter_example():
    two_star_solution = two_star()
    how_far = two_star_solution * 10

    print(starting_nodes)

    current_nodes = starting_nodes
    for i in range(how_far):
        for idx, node in enumerate(current_nodes):
            current_nodes[idx] = graph[node][next(instructions)]
        print(current_nodes)
        if np.all([node[-1] == 'Z' for node in current_nodes]):
            print('Made it out of the desert')
            break


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
