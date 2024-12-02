import numpy as np


def read_input(fname):
    with open(fname) as file:
        return [[int(x) for x in line.split()] for line in file.readlines()]


def process(x):
    result = []
    y = np.array(x)
    result.append(y)
    while True:
        y = y[1:] - y[:-1]
        result.append(y)
        if all(y == 0):
            break
    previous = result[-1][-1]
    for i in range(0, len(result)-1)[::-1]:
        previous = result[i][-1] + previous
    return previous


def part_1(x):
    return sum(process(y) for y in x)


def part_2(x):
    return sum(process(y[::-1]) for y in x)


if __name__ == "__main__":
    print("Part 1 test:", part_1(read_input("test.txt")))
    print("Part 1:", part_1(read_input("input.txt")))
    print("Part 2 test:", part_2(read_input("test.txt")))
    print("Part 2:", part_2(read_input("input.txt")))
