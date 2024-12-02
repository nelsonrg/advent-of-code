import numpy as np
from itertools import combinations


def read_input(fname):
    with open(fname) as file:
        return np.array([[x for x in line.strip()] for line in file.readlines()])


def get_distance(p1, p2, is_empty_rows, is_empty_cols, n):
    r0 = min(p1[0], p2[0])
    r1 = max(p1[0], p2[0])
    delta_r = r1 - r0 + (n-1)*sum(is_empty_rows[r0:r1])

    c0 = min(p1[1], p2[1])
    c1 = max(p1[1], p2[1])
    delta_c = c1 - c0 + (n-1)*sum(is_empty_cols[c0:c1])

    return delta_r + delta_c


def day11(x, n):
    y = x.copy()
    y[np.where(y == ".")] = 0
    y[np.where(y == "#")] = 1
    y = y.astype(int)

    is_empty_r = (np.sum(y, 1) == 0).astype(int)
    is_empty_c = (np.sum(y, 0) == 0).astype(int)

    galaxies = np.where(y == 1)
    galaxies = [(r, c) for r, c in zip(*galaxies)]
    combos = combinations(galaxies, 2)

    return sum(get_distance(g1, g2, is_empty_r, is_empty_c, n) for g1, g2 in combos)


if __name__ == "__main__":
    print("Part 1 test:", day11(read_input("test.txt"), 2))
    print("Part 1:", day11(read_input("input.txt"), 2))
    print()
    print("Part 2 test:", day11(read_input("test.txt"), 100))
    print("Part 2:", day11(read_input("input.txt"), int(1e6)))
