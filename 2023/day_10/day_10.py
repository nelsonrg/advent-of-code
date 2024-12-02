import numpy as np
from functools import reduce
from skimage.morphology import flood_fill
import matplotlib.pyplot as plt
np.set_printoptions(edgeitems=10, linewidth=180)


d = {
    "north": (-1, 0),
    "south": (1, 0),
    "west": (0, -1),
    "east": (0, 1)
}


converter = {
    "|": {"north": "north", "south": "south"},
    "-": {"east": "east", "west": "west"},
    "L": {"west": "north", "south": "east"},
    "J": {"east": "north", "south": "west"},
    "7": {"east": "south", "north": "west"},
    "F": {"north": "east", "west": "south"}
}


def read_input(fname):
    with open(fname) as file:
        return np.array([[x for x in line.strip()] for line in file.readlines()])


def move_location(start, direction):
    move = d[direction]
    end = (start[0] + move[0], start[1] + move[1])
    if end[0] < 0 or end[1] < 0:
        return None
    return end


def build_path(x, direction):
    y = np.zeros_like(x, dtype="int")
    start = np.where(x == "S")
    start = (start[0][0], start[1][0])

    step = 0
    y[start] = step
    location = move_location(start, direction)

    while x[location] != "S":
        step += 1
        y[location] = step
        symbol = x[location]
        direction = converter[symbol][direction]
        location = move_location(location, direction)
    return y


def get_minimum_steps(x):
    start = np.where(x == "S")
    start = (start[0][0], start[1][0])

    possible_directions = [
        direction for direction in d
        if move_location(start, direction) is not None and
        converter.get(x[move_location(start, direction)]) is not None and
        converter.get(x[move_location(start, direction)]).get(direction) is not None
    ]

    return reduce(
        np.minimum,
        [build_path(x, direction) for direction in possible_directions]
    )


def part_1(x):
    return np.max(get_minimum_steps(x))


def find_replacement(x):
    # find what letter replaces S
    start = np.where(x == "S")
    start = (start[0][0], start[1][0])

    possible_directions = [
        direction for direction in d
        if move_location(start, direction) is not None and
        converter.get(x[move_location(start, direction)]) is not None and
        converter.get(x[move_location(start, direction)]).get(direction) is not None
    ]

    replacement = None
    for symbol, routes in converter.items():
        if all(direction in routes.values() for direction in possible_directions):
            replacement = symbol
    return replacement


def part_2(x, verbose=False):
    start = np.where(x == "S")
    start = (start[0][0], start[1][0])

    y = get_minimum_steps(x)
    y = (y > 0).astype(int)
    y[start] = 1

    # this solution requires replacing S with the correct symbol
    x[np.where(x == "S")] = find_replacement(x)

    z = np.zeros_like(y)
    total = 0
    for i in range(x.shape[0]):
        is_in = False
        for j in range(x.shape[1]):
            if y[i, j]:
                if x[i, j] in "|F7":  # can also use "|JL"
                    is_in = not is_in
            else:
                total += is_in
                z[i, j] = is_in
    if verbose:
        print()
        print(z)
    return total


def ffill(x):
    y = x.copy()
    step = 0
    while 0 in y:
        # find zeros
        zeros = np.where(y == 0)
        first_zero = (zeros[0][0], zeros[1][0])
        y = flood_fill(y, first_zero, -2)
        new_fills = np.where(y == -2)
        if (min(new_fills[0]) == 0 or max(new_fills[0]) == y.shape[0]-1 or
            min(new_fills[1]) == 0 or max(new_fills[1]) == y.shape[1]-1):
            # then these are outside
            y[new_fills] = -1
        else:
            y[new_fills] = 2
        step += 1
    print("\tNumber of flood fill steps:", step)
    return y


def part_2_2(x, verbose=False, box=False):
    # find replacement for S
    replacement = find_replacement(x)

    # dilate the matrix
    y = np.full((x.shape[0]*2, x.shape[1]*2), ".")
    h = x.shape[0]
    w = x.shape[1]
    for i in range(h):
        for j in range(w):
            value = x[i, j]
            y[2*i, 2*j] = value
            if value == "S":
                value = replacement
            if value != "." and "east" in converter[value].values():
                y[2*i, 2*j+1] = "-"
            if value != "." and "south" in converter[value].values():
                y[2*i+1, 2*j] = "|"

    if verbose:
        print(y)

    start = np.where(y == "S")
    start = (start[0][0], start[1][0])

    z = build_path(y, list(converter[replacement].values())[0])
    z = (z > 0).astype(int)
    z[start] = 1

    # now flood fill and check if it is outside
    final = ffill(z)
    if verbose:
        print(final)
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(final)
    ax[1].imshow(final[::2, ::2])
    ax[0].set_title("Upsampled x2")
    ax[1].set_title("Flood-Filled Path")
    if box:
        ax[1].plot((35, 105), (105, 105), 'r-')
        ax[1].plot((35, 35), (105, 35), 'r-')
        ax[1].plot((105, 105), (35, 105), 'r-')
        ax[1].plot((105, 35), (35, 35), 'r-')
        ax[1].plot((70), (70), 'ro')
    return np.sum(np.concatenate(final[::2, ::2] == 2))


if __name__ == "__main__":
    print("Part 1 test 1:", part_1(read_input("test1.txt")))
    print("Part 1 test 2:", part_1(read_input("test2.txt")))
    print("Part 1:", part_1(read_input("input.txt")))
    print()
    print("Part 2 test 1:", part_2(read_input("test3.txt"), verbose=False))
    print("Part 2 test 2:", part_2(read_input("test4.txt"), verbose=False))
    print("Part 2 test 2:", part_2(read_input("test5.txt"), verbose=False))
    print("Part 2:", part_2(read_input("input.txt")))
    print()
    print("Part 2 flood fill test 1:", part_2_2(read_input("test3.txt"), verbose=False))
    print("Part 2 flood fill test 2:", part_2_2(read_input("test4.txt"), verbose=False))
    print("Part 2 flood fill test 3:", part_2_2(read_input("test5.txt"), verbose=False))
    print("Part 2 flood fill:", part_2_2(read_input("input.txt"), box=True))
    plt.show()
