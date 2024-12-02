from functools import reduce
from operator import mul
from math import sqrt, floor, ceil


def read_input(fname):
    time = []
    distance = []
    with open(fname) as file:
        for line in file.readlines():
            if "Time:" in line:
                time = [int(x) for x in line.split(":")[-1].split()]
            elif "Distance:" in line:
                distance = [int(x) for x in line.split(":")[-1].split()]
    return time, distance


def process_race_bruteforce(time, distance):
    first = None
    last = None
    # find first occurence
    for t in range(1, time):
        d = (time - t) * t
        if d > distance:
            first = t
            break
    # find last occurence
    for t in range(time-1, first, -1):
        d = (time - t) * t
        if d > distance:
            last = t
            break
    return last - first + 1


def process_race(time, distance):
    offset = sqrt(time**2 - 4*distance)
    roots = ((time - offset)/2, (time + offset)/2)
    if roots[0].is_integer():
        start = int(roots[0]) + 1
    else:
        start = ceil(roots[0])
    if roots[1].is_integer():
        end = int(roots[1]) - 1
    else:
        end = floor(roots[1])
    return end - start + 1


def part_1(times, distances):
    return reduce(mul, [process_race(t, d) for t, d in zip(times, distances)])


def part_2(times, distances):
    return process_race(int("".join([str(x) for x in times])), int("".join([str(x) for x in distances])))


if __name__ == "__main__":
    print("Part 1 test:", part_1(*read_input("test.txt")))
    print("Part 1:", part_1(*read_input("input.txt")))
    print("Part 2:", part_2(*read_input("input.txt")))
