import logging
import re
import sys
import time
from collections import ChainMap, Counter
from enum import IntEnum
from functools import total_ordering
from pathlib import Path

import numpy as np

test_answer = 4361


class Card(IntEnum):
    J = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    T = 10
    Q = 11
    K = 12
    A = 13


num2str = {
    "2": "TWO",
    "3": "THREE",
    "4": "FOUR",
    "5": "FIVE",
    "6": "SIX",
    "7": "SEVEN",
    "8": "EIGHT",
    "9": "NINE",
}


@total_ordering
class CamelCard:
    def __init__(self, card_str: str):
        self.card_str = card_str
        try:
            self.card = getattr(Card, card_str)
        except AttributeError:
            self.card = getattr(Card, num2str[card_str])

    def __str__(self):
        return self.card_str

    def __repr__(self):
        return self.card_str

    def __lt__(self, other):
        return self.card < other.card

    def __eq__(self, other):
        return self.card == other.card

    def __hash__(self):
        return hash(self.card)


class Hand(IntEnum):
    high_card = 1
    one_pair = 2
    two_pair = 3
    three_of_a_kind = 4
    full_house = 5
    four_of_a_kind = 6
    five_of_a_kind = 7


@total_ordering
class CamelHand:
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
            return Hand.five_of_a_kind
        if mc[0][1] == 4:
            if mc[1][0] == j or mc[0][0] == j:
                return Hand.five_of_a_kind
            return Hand.four_of_a_kind
        if mc[0][1] == 3:
            if mc[1][1] == 2:
                if mc[0][0] == j or mc[1][0] == j:
                    return Hand.five_of_a_kind
                return Hand.full_house
            if mc[0][0] == j or mc[1][0] == j or mc[2][0] == j:
                return Hand.four_of_a_kind
            return Hand.three_of_a_kind
        if mc[0][1] == 2:
            if mc[1][1] == 2:
                if mc[0][0] == j or mc[1][0] == j:
                    return Hand.four_of_a_kind
                if mc[2][0] == j:
                    return Hand.full_house
                return Hand.two_pair
            if j in [c[0] for c in mc]:
                return Hand.three_of_a_kind
            return Hand.one_pair
        if j in [c[0] for c in mc]:
            return Hand.one_pair
        return Hand.high_card

    def __str__(self):
        return f"Hand: {''.join([str(c) for c in self.hand])}\tType: {self.type.name}\tBit: {self.bid}"

    def __repr__(self):
        return f"Hand: {''.join([str(c) for c in self.hand])};Bit: {self.bid}"

    def __lt__(self, other):
        self_index = self.type.value
        other_index = other.type.value
        if self.type != other.type:
            return self.type < other.type

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
    #  print([h.type.name for h in hands])
    sorted_hands = sorted(hands)
    print(*sorted_hands, sep="\n")
    #  print([h.type.name for h in sorted_hands])

    sorted_hand_values = [hand.bid * (idx + 1) for idx, hand in enumerate(sorted_hands)]
    #  print(sorted_hand_values)
    answer = sum(sorted_hand_values)
    print(answer)


def two_star():
    pass


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"It took {end_time - start_time} seconds")
