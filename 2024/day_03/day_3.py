import re
from operator import mul
from functools import reduce


def read_input(file_name):
    with open(file_name) as f:
        return f.read().strip()


def part_1(memory):
    matches = re.findall(r"mul\((\d+,\d+)\)", memory)
    pairs = map(lambda pair: map(int, pair.split(",")), matches)
    multiplications = map(lambda pair: reduce(mul, pair), pairs)
    aggregate = sum(multiplications)
    return aggregate


def part_2(memory):
    matches = re.findall(r"mul\((\d+,\d+)\)|(do\(\))|(don't\(\))", memory)
    enabled = True
    total = 0
    for pair, do, dont in matches:
        if dont:
            enabled = False
        elif do:
            enabled = True
        else:
            if enabled:
                total += reduce(mul, map(int, pair.split(",")))
    return total


if __name__ == "__main__":
    memory = read_input("day_3_input.txt")
    print(part_1(memory))
    print(part_2(memory))
