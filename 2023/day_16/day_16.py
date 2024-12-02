import numpy as np


def read_input(fname):
    result = []
    with open(fname) as file:
        for line in file.readlines():
            mirrors = list(line.strip())
            result.append(mirrors)
    return np.array(result)


def pretty_print(x):
    print()
    print('\n'.join(''.join(str(y) for y in row) for row in x))


class MirrorGrid:
    redirect = {
        "\\": {
            "up": ("left",),
            "down": ("right",),
            "right": ("down",),
            "left": ("up",)
        },
        "/": {
            "up": ("right",),
            "down": ("left",),
            "right": ("up",),
            "left": ("down",)
        },
        "-": {
            "up": ("left", "right"),
            "down": ("left", "right"),
            "right": ("right",),
            "left": ("left",)
        },
        "|": {
            "up": ("up",),
            "down": ("down",),
            "right": ("up", "down"),
            "left": ("up", "down")
        },
        ".": {
            "up": ("up",),
            "down": ("down",),
            "right": ("right",),
            "left": ("left",)
        }
    }

    direction_converter = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    def __init__(self, x):
        self.grid = x
        self.energized = np.zeros_like(self.grid, dtype="int")

    def path_light(self, start=(0, 0), direction="right"):
        current = [(start, direction)]
        memo = {}
        while current:
            c = current.pop()
            self.energized[c[0]] = 1
            next_step = self.step(*c, memo)
            current += next_step

    def step(self, loc, input_direction, memo):
        if (loc, input_direction) in memo:
            return []
        else:
            memo[(loc, input_direction)] = 1
        output_direction = MirrorGrid.redirect[self.grid[loc]][input_direction]
        output_direction_n = tuple(MirrorGrid.direction_converter[d]
                                   for d in output_direction)
        next_step = tuple(tuple(np.add(loc, d)) for d in output_direction_n)
        return [(n, d) for n, d in zip(next_step, output_direction)
                if -1 < n[0] < self.grid.shape[0] and -1 < n[1] < self.grid.shape[1]]

    def reset_energized(self):
        self.energized = np.zeros_like(self.grid, dtype="int")


def part_1(x):
    grid = MirrorGrid(x)
    grid.path_light()
    return np.sum(grid.energized)


def part_2(x):
    energized = []
    grid = MirrorGrid(x)
    width = x.shape[1]
    height = x.shape[0]
    for i in range(height):
        grid.reset_energized()
        grid.path_light((i, 0), direction="right")
        energized.append(np.sum(grid.energized))
        grid.reset_energized()
        grid.path_light((i, width-1), direction="left")
        energized.append(np.sum(grid.energized))
    for j in range(width):
        grid.reset_energized()
        grid.path_light((0, j), direction="down")
        energized.append(np.sum(grid.energized))
        grid.reset_energized()
        grid.path_light((height-1, j), direction="up")
        energized.append(np.sum(grid.energized))
    return max(energized)


if __name__ == "__main__":
    print("Part 1 test:", part_1(read_input("test.txt")))
    print("Part 1:", part_1(read_input("input.txt")))
    print()
    print("Part 2 test:", part_2(read_input("test.txt")))
    print("Part 2:", part_2(read_input("input.txt")))
