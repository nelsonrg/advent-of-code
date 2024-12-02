import numpy as np


def read_input(fname):
    result = []
    with open(fname) as file:
        for line in file.readlines():
            springs = list(line.strip())
            result.append(springs)
    return np.array(result)


def tilt(x):
    height = x.shape[0]
    width = x.shape[1]
    y = x.copy()
    y[np.where(y == "O")] = "."
    for c in range(width):
        cubes = list(np.where(x[:, c] == "#")[0])
        cubes.append(height)
        last_cube = -1
        for cube in cubes:
            n = sum(x[last_cube+1:cube, c] == "O")
            y[last_cube+1:last_cube+1+n, c] = "O"
            last_cube = cube
    return y


def score(x):
    return sum(x.shape[0] - np.where(x == "O")[0])


def pretty_print(x):
    print()
    print('\n'.join(''.join(str(y) for y in row) for row in x))


def rotate(x):
    return np.rot90(x, axes=(1, 0))


def cycle(x):
    for i in range(4):
        x = tilt(x)
        x = rotate(x)

    return x


def find_cycle(x, total):
    t = 0
    seen = {}
    while t < total:
        t += 1
        x = cycle(x)
        hashable_x = tuple(tuple(row) for row in x)
        if hashable_x in seen:
            print(f"\tCycle found in {t} steps.")
            return t - seen[hashable_x], t, x
        else:
            seen[hashable_x] = t
    return None


def part_1(x):
    return score(tilt(x))


def part_2(x, total):
    cycle_length, t_start, x_start = find_cycle(x, total)
    print("\tCycle length is", cycle_length)
    delta_t = total - (
        ((total - t_start) // cycle_length)*cycle_length + t_start)
    for _ in range(delta_t):
        x_start = cycle(x_start)
    return score(x_start)


if __name__ == "__main__":
    print("Part 1 test:", part_1(read_input("test.txt")))
    print("Part 1:", part_1(read_input("input.txt")))
    print()
    print("Part 2 test:", part_2(read_input("test.txt"), int(1e9)))
    print("Part 2:", part_2(read_input("input.txt"), int(1e9)))
    print()
    for t in range(3, 10):
        print(f"Part 2 {t}:", part_2(read_input("input.txt"), int(1*10**t)))
