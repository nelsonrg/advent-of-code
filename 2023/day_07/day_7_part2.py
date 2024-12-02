from collections import Counter
import itertools
from math import log


STRENGTH = {"A": 14,
            "K": 13,
            "Q": 12,
            "J": 1,
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


# this idea is from Harrison Leinweber.
# huge performance improvement
def score_hand(hand):
    card_counter = Counter(hand)
    most_common = card_counter.most_common(1)[0]
    if most_common[0] == "J":
        most_common = card_counter.most_common(2)[-1]
    new_hand = hand.replace("J", most_common[0])
    return score_hand_helper(new_hand)


def entropy(frequencies):
    probs = [freq / len(frequencies) for freq in frequencies]
    return -1*sum(p*log(p) for p in probs)


def score_hand_helper(hand):
    card_counter = Counter(hand)
    return -1*entropy(card_counter.values())


def sort_hands(hands, bids):
    scores = [score_hand(h) for h in hands]
    strengths = [[STRENGTH[c] for c in h] for h in hands]

    return sorted(zip(scores, strengths, bids))


def part_2(x):
    hands, bids = zip(*x)
    sorted_hands = sort_hands(hands, bids)

    return sum(bid * (i + 1) for i, (_, _, bid) in enumerate(sorted_hands))


if __name__ == "__main__":
    print("Part 2 test:", part_2(read_input("test.txt")))
    print("Part 2:", part_2(read_input("input.txt")))
