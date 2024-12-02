import numpy as np


def read_input(fname):
    results = []
    with open(fname) as file:
        for line in file.readlines():
            x = line.strip().split()
            results.append((x[0], int(x[1]), x[2][1:-1]))
    return results


DIRECTION = {
    "D": (1, 0),
    "U": (-1, 0),
    "R": (0, 1),
    "L": (0, -1)
}

DIRECTION2 = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U"
}


def get_vertex(start, direction, distance):
    x, y = start
    dx, dy = DIRECTION[direction]
    return x+dx*distance, y+dy*distance


def shoelace(vertices):
    s1, s2 = zip(*vertices)
    s1 = np.array(s1)
    s2 = np.array(s2)
    return 1/2 * abs(sum(s1[:-1]*s2[1:]) - sum(s1[1:]*s2[:-1]))


def calculate_area(vertices, perimeter):
    return shoelace(vertices) + perimeter//2 + 1


def part_1(instructions):
    x, y = 0, 0
    vertices = [(x, y)]
    perimeter = 0
    for direction, distance, _ in instructions:
        perimeter += distance
        x, y = get_vertex((x, y), direction, distance)
        vertices.append((x, y))
    return calculate_area(vertices, perimeter)


def part_2(instructions):
    # get new instructions from hex
    ins = [(DIRECTION2[i[-1][-1]], int(i[-1][1:-1], 16)) for i in instructions]

    x, y = 0, 0
    vertices = [(x, y)]
    perimeter = 0
    for direction, distance in ins:
        perimeter += distance
        x, y = get_vertex((x, y), direction, distance)
        vertices.append((x, y))
    return calculate_area(vertices, perimeter)


if __name__ == "__main__":
    print("Part 1 test:", part_1(read_input("test.txt")))
    print("Part 1:", part_1(read_input("input.txt")))
    print()
    print("Part 2 test:", part_2(read_input("test.txt")))
    print("Part 2:", part_2(read_input("input.txt")))
