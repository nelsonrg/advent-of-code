from collections import Counter
from math import log


STRENGTH = {"A": 14,
            "K": 13,
            "Q": 12,
            "J": 11,
            "T": 10,
            "9": 9,
            "8": 8,
            "7": 7,
            "6": 6,
            "5": 5,
            "4": 4,
            "3": 3,
            "2": 2}


def read_input(fname):
    with open(fname) as file:
        return [(line.split()[0], int(line.split()[1])) for line in file.readlines()]


def entropy(frequencies):
    probs = [freq / len(frequencies) for freq in frequencies]
    return -1*sum(p*log(p) for p in probs)


def score_hand(hand):
    card_counter = Counter(hand)
    return -1*entropy(card_counter.values())


def sort_hands(hands, bids):
    scores = [score_hand(h) for h in hands]
    strengths = [[STRENGTH[c] for c in h] for h in hands]

    return sorted(zip(scores, strengths, bids))


def part_1(x):
    hands, bids = zip(*x)
    sorted_hands = sort_hands(hands, bids)

    return sum(bid * (i + 1) for i, (_, _, bid) in enumerate(sorted_hands))


if __name__ == "__main__":
    print("Part 1 test:", part_1(read_input("test.txt")))
    print("Part 1:", part_1(read_input("input.txt")))
