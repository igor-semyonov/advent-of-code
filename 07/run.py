import logging
import re
import sys
import time
from collections import ChainMap, Counter
from functools import total_ordering
from pathlib import Path

import numpy as np

test_answer = 4361


@total_ordering
class CamelCard:
    order = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]

    def __init__(self, card: str):
        self.card = card

    def __str__(self):
        return self.card

    def __repr__(self):
        return self.card

    def __lt__(self, other):
        self_index = self.order.index(self.card)
        other_index = self.order.index(other.card)
        return self_index < other_index

    def __eq__(self, other):
        return self.card == other.card

    def __hash__(self):
        return hash(self.card)


@total_ordering
class CamelHand:
    order = [
        "high-card",
        "one-pair",
        "two-pair",
        "three-of-a-kind",
        "full-house",
        "four-of-a-kind",
        "five-of-a-kind",
    ]
    joker = CamelCard("J")

    def __init__(self, hand_string):
        self.hand, bid = hand_string.split()
        self.hand = [CamelCard(c) for c in self.hand]
        self.bid = int(bid)
        self.type = self.calculate_type()

    def calculate_type(self):
        joking = self.joker in self.hand
        j = self.joker
        counter = Counter(self.hand)
        mc = counter.most_common()
        if mc[0][1] == 5:
            return "five-of-a-kind"
        if mc[0][1] == 4:
            if mc[1][0] == j or mc[0][0] == j:
                return "five-of-a-kind"
            return "four-of-a-kind"
        if mc[0][1] == 3:
            if mc[1][1] == 2:
                if mc[0][0] == j or mc[1][0] == j:
                    return "five-of-a-kind"
                return "full-house"
            if mc[0][0] == j or mc[1][0] == j or mc[2][0] == j:
                return "four-of-a-kind"
            return "three-of-a-kind"
        if mc[0][1] == 2:
            if mc[1][1] == 2:
                if mc[0][0] == j or mc[1][0] == j:
                    return "four-of-a-kind"
                if mc[2][0] == j:
                    return "full-house"
                return "two-pair"
            if j in [c[0] for c in mc]:
                return "three-of-a-kind"
            return "one-pair"
        if j in [c[0] for c in mc]:
            return "one-pair"
        return "high-card"

    def __str__(self):
        return f"Hand: {''.join([str(c) for c in self.hand])}\tBit: {self.bid}"

    def __repr__(self):
        return f"Hand: {''.join([str(c) for c in self.hand])};Bit: {self.bid}"

    def __lt__(self, other):
        self_index = self.order.index(self.type)
        other_index = self.order.index(other.type)
        if self_index != other_index:
            return self_index < other_index

        for card, other_card in zip(self.hand, other.hand):
            if card < other_card:
                return True
            elif card > other_card:
                return False


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

    one_star()


def one_star():
    hands = list(map(CamelHand, lines))
    print(*hands, sep="\n")
    print([h.type for h in hands])
    sorted_hands = sorted(hands)
    print(*sorted_hands, sep="\n")
    print([h.type for h in sorted_hands])

    sorted_hand_values = [hand.bid * (idx + 1) for idx, hand in enumerate(sorted_hands)]
    print(sorted_hand_values)
    answer = sum(sorted_hand_values)
    print(answer)


def two_star():
    pass


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
