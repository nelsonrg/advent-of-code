import re
from itertools import product
from functools import cache


def read_input(fname):
    result = []
    with open(fname) as file:
        for line in file.readlines():
            springs, numbers = line.strip().split()
            numbers = [int(x) for x in numbers.split(",")]
            result.append((springs, numbers))
    return result


def validate(springs, numbers):
    broken = re.findall("#+", springs)
    return list(map(len, broken)) == numbers


def count_arrangement(springs, numbers):
    count = 0
    for p in product(*[".#" if c == "?" else c for c in springs]):
        if validate("".join(p), numbers):
            count += 1
    return count


@cache
def count_arrangement2(springs, group_count, counts):
    # at end of the row
    if not springs:
        count = not counts
    # at a broken spring
    elif springs[0] == "#":
        count = count_arrangement2(springs[1:], group_count + 1, counts)
    # between sequences
    elif springs[0] == "." or not counts:
        if counts and group_count == counts[0]:
            count = count_arrangement2(springs[1:], 0, counts[1:])
        elif group_count == 0:
            count = count_arrangement2(springs[1:], 0, counts)
        else:
            count = 0
    # at question mark
    else:
        # arrangements if ? == #
        broken_count = count_arrangement2(springs[1:], group_count + 1, counts)
        # arrangements if ? == .
        intact_count = 0
        if group_count == counts[0]:
            intact_count = count_arrangement2(springs[1:], 0, counts[1:])
        elif group_count == 0:
            intact_count = count_arrangement2(springs[1:], 0, counts)
        count = broken_count + intact_count
    return count


def count_arrangement3(springs, group_count, counts, memo):
    if (springs, group_count, counts) in memo:
        return memo.get((springs, group_count, counts))
    # at end of the row
    if not springs:
        count = not counts
    # at a broken spring
    elif springs[0] == "#":
        count = count_arrangement3(springs[1:], group_count + 1, counts, memo)
    # between sequences
    elif springs[0] == "." or not counts:
        if counts and group_count == counts[0]:
            count = count_arrangement3(springs[1:], 0, counts[1:], memo)
        elif group_count == 0:
            count = count_arrangement3(springs[1:], 0, counts, memo)
        else:
            count = 0
    # at question mark
    else:
        # arrangements if ? == #
        broken_count = count_arrangement3(springs[1:], group_count + 1, counts, memo)
        # arrangements if ? == .
        intact_count = 0
        if group_count == counts[0]:
            intact_count = count_arrangement3(springs[1:], 0, counts[1:], memo)
        elif group_count == 0:
            intact_count = count_arrangement3(springs[1:], 0, counts, memo)
        count = broken_count + intact_count
    memo[(springs, group_count, counts)] = count
    return count


def part_1(x):
    return sum(count_arrangement(s, n) for s, n in x)


def part_2(x):
    springs, numbers = zip(*x)
    springs = [(s+"?")*5 for s in springs]
    numbers = [n*5 for n in numbers]
    return sum(count_arrangement2(s, 0, tuple(n))
               for s, n in zip(springs, numbers))


def part_2_exp(x):
    springs, numbers = zip(*x)
    springs = [(s+"?")*5 for s in springs]
    numbers = [n*5 for n in numbers]
    memo = {}
    return sum(count_arrangement3(s, 0, tuple(n), memo)
               for s, n in zip(springs, numbers))


if __name__ == "__main__":
    print("Part 1 test:", part_1(read_input("test.txt")))
    print("Part 1:", part_1(read_input("input.txt")))
    print()
    print("Part 2 test:", part_2(read_input("test.txt")))
    print("Part 2:", part_2(read_input("input.txt")))
    print()
    print("Part 2 experiment test:", part_2_exp(read_input("test.txt")))
    print("Part 2 experiment:", part_2_exp(read_input("input.txt")))
