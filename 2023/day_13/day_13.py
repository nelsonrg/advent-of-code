import numpy as np


def read_input(fname):
    result = []
    block = []
    with open(fname) as file:
        for line in file.readlines():
            springs = line.strip()
            if not springs:
                result.append(np.array(block))
                block = []
            else:
                block.append(list(springs))
    return result


def is_h_symmetric(x, c):
    left = x[:, c:]
    right = x[:, :c][:, ::-1]
    new_width = min(left.shape[1], right.shape[1])
    return np.all(left[:, :new_width] == right[:, :new_width])


def find_reflection(b, ignore=None):
    width = b.shape[1]
    for w in range(1, width):
        if is_h_symmetric(b, w) and (w, 0) != ignore:
            return (w, 0)
    height = b.shape[0]
    for h in range(1, height):
        if is_h_symmetric(np.transpose(b), h) and (0, h) != ignore:
            return (0, h)
    return None


def part_1(x):
    results = [find_reflection(b) for b in x]
    h, v = zip(*results)
    return sum(h) + sum(v)*100


def find_new_reflection(b):
    original_reflection = find_reflection(b)
    c = (b == ".").astype(int)
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            d = c.copy()
            d[i, j] = 1 - d[i, j]
            reflection = find_reflection(d, ignore=original_reflection)
            if reflection is not None and reflection != original_reflection:
                return reflection
    return None


def part_2(x):
    results = [find_new_reflection(b) for b in x]
    h, v = zip(*results)
    return sum(h) + sum(v)*100


if __name__ == "__main__":
    print("Part 1 test:", part_1(read_input("test.txt")))
    print("Part 1:", part_1(read_input("input.txt")))
    print()
    print("Part 2 test:", part_2(read_input("test.txt")))
    print("Part 2:", part_2(read_input("input.txt")))
