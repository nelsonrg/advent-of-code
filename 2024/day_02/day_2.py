from itertools import pairwise


def read_input(file_name):
    with open(file_name) as f:
        reports = [[int(level) for level in report.split()]
                   for report in f.readlines()]
    return reports


def part_1(reports):
    return sum(map(is_safe, reports))


def is_safe(report):
    return (is_strictly_monotonic(report) and
            is_difference_between_range(report, min_delta=1, max_delta=3))


def is_strictly_monotonic(sequence):
    deltas = tuple(map(lambda x: x[1] - x[0], pairwise(sequence)))
    return (
        all(map(lambda delta: delta > 0, deltas)) or
        all(map(lambda delta: delta < 0, deltas))
    )


def is_difference_between_range(sequence, min_delta=1, max_delta=3):
    deltas = map(lambda x: x[1] - x[0], pairwise(sequence))
    abs_deltas = map(abs, deltas)
    return all(map(lambda delta: min_delta <= delta <= max_delta, abs_deltas))


def part_2(reports):
    return sum(map(is_safe_with_dampener, reports))


def is_safe_with_dampener(report):
    if is_safe(report):
        return True
    for i in range(len(report)):
        if is_safe(report[:i] + report[i+1:]):
            return True
    return False


if __name__ == "__main__":
    reports = read_input("day_2_input.txt")
    print(part_1(reports))
    print(part_2(reports))
