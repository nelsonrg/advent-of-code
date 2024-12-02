import numpy as np
from itertools import chain


def read_input(fname):
    with open(fname) as file:
        return np.array([list(x.strip()) for x in file.readlines()])


def find_reachable_points(x):
    reachable_plots = {}
    height = x.shape[0]
    width = x.shape[1]
    for i in range(height):
        for j in range(width):
            point = (i, j)
            reachable_plots[point] = []
            # up
            if i > 0 and x[i-1, j] in ".S":
                reachable_plots[point].append((i-1, j))
            # down
            if i < height - 1 and x[i+1, j] in ".S":
                reachable_plots[point].append((i+1, j))
            # left
            if j > 0 and x[i, j-1] in ".S":
                reachable_plots[point].append((i, j-1))
            # right
            if j < width - 1 and x[i, j+1] in ".S":
                reachable_plots[point].append((i, j+1))
    return reachable_plots


def part_1(x, n_steps):
    reachable_plots = find_reachable_points(x)
    start = np.where(x == "S")
    current = set([(start[0][0], start[1][0])])
    for step in range(n_steps):
        current = set(chain(*(reachable_plots[point] for point in current)))
    return len(current)


def find_reachable_points2(x):
    reachable_plots = {}
    height = x.shape[0]
    width = x.shape[1]
    for i in range(height):
        for j in range(width):
            point = (0, 0, i, j)
            reachable_plots[point] = []
            # up
            if i > 0 and x[i-1, j] in ".S":
                reachable_plots[point].append((0, 0, i-1, j))
            elif i == 0 and x[-1, j] in ".S":
                reachable_plots[point].append((-1, 0, height-1, j))
            # down
            if i < height - 1 and x[i+1, j] in ".S":
                reachable_plots[point].append((0, 0, i+1, j))
            elif i == height - 1 and x[0, j] in ".S":
                reachable_plots[point].append((1, 0, 0, j))
            # left
            if j > 0 and x[i, j-1] in ".S":
                reachable_plots[point].append((0, 0, i, j-1))
            elif j == 0 and x[i, -1] in ".S":
                reachable_plots[point].append((0, -1, i, width-1))
            # right
            if j < width - 1 and x[i, j+1] in ".S":
                reachable_plots[point].append((0, 0, i, j+1))
            elif j == width - 1 and x[i, 0] in ".S":
                reachable_plots[point].append((0, 1, i, 0))
    return reachable_plots


def get_reachable_points(point, reachable_points):
    map_y, map_x, y, x = point
    next_points = reachable_points[(0, 0, y, x)]
    return [(map_y+map_dy, map_x+map_dx, y, x) for map_dy, map_dx, y, x
            in next_points]


def part_2_helper(x, n_steps):
    reachable_plots = find_reachable_points2(x)
    start = np.where(x == "S")
    current = set([(0, 0, start[0][0], start[1][0])])
    steps = []
    values = []
    for step in range(n_steps):
        current = set(
            chain(*(get_reachable_points(point, reachable_plots)
                    for point in current))
        )
        steps.append(step)
        values.append(len(current))
    return steps, values


# needed help on this one.
# had the right idea with the recurrence (see notebooks and R code)
def part_2(x, n_steps):
    s = 500
    steps, values = part_2_helper(x, s)
    steps = np.array(steps)
    values = np.array(values)
    width = x.shape[0]
    X = np.arange(width // 2 - 1, s, width)
    y = values[X]
    X = np.arange(0, X.shape[0])
    p = np.poly1d(np.polyfit(X, y, 2))
    N = (n_steps - width//2) / width
    return p(N)


if __name__ == "__main__":
    print("Part 1 test 1:", part_1(read_input("test.txt"), 6))
    print("Part 1:", part_1(read_input("input.txt"), 64))
    print()
    print("Part 2:", part_2(read_input("input.txt"), 26501365))
    """
    test_numbers = (6, 10, 50, 100, 500)
    expected = (16, 50, 1594, 6536, 167004)
    for n, ex in zip(test_numbers, expected):
        print(f"Part 2 n = {n}: {part_2(read_input('test.txt'), n)}",
              "Expected:", ex)
    """
