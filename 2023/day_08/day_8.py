from itertools import cycle
from math import lcm
import time


def read_input(fname):
    directions = None
    instructions = {}
    with open(fname) as file:
        i = 0
        for line in file.readlines():
            if i == 0:
                directions = line.strip()
                converter = {"L": 0, "R": 1}
                directions = [converter[c] for c in directions]
            elif i > 1:
                element, inst = line.strip().split(" = ")
                inst = inst.split(", ")
                instructions[element] = tuple(ins.strip("()") for ins in inst)
            i += 1
    return directions, instructions


def part_1(directions, instructions):
    direction = cycle(directions)
    search = "AAA"
    steps = 0
    while search != "ZZZ":
        search = instructions[search][next(direction)]
        steps += 1
    return steps


def part_2_helper(directions, instructions, search):
    direction = cycle(directions)
    steps = 0
    while search[-1] != "Z":
        search = instructions[search][next(direction)]
        steps += 1
    return steps


def part_2(directions, instructions):
    search = [k for k in instructions.keys() if k[-1] == "A"]
    print("Starting nodes:", search)
    num_steps = [part_2_helper(directions, instructions, s) for s in search]
    print("Length of directions:", len(directions))
    print("Number of steps in cycles:", num_steps)
    print("Steps / Length of Directions", [n / len(directions) for n in num_steps])
    # math is easy
    return lcm(*num_steps)


def time_the_code(directions, instructions):
    direction = cycle(directions)
    search = [k for k in instructions.keys() if k[-1] == "A"][0]
    steps = 0
    max_steps = 1e6
    start = time.time_ns()
    while True:
        search = instructions[search][next(direction)]
        steps += 1
        if steps > max_steps:
            break
    end = time.time_ns()
    total_time = end - start
    part2_answer = part_2(directions, instructions)
    rate = max_steps / total_time
    print("Time to brute force part 2 (approximate):",
          part2_answer / rate * 1e-9 / 60 / 60 / 24, "days")


if __name__ == "__main__":
    print("Part 1 test:", part_1(*read_input("test.txt")))
    print("Part 1:", part_1(*read_input("input.txt")))
    print()
    print("Part 2 test:", part_2(*read_input("test2.txt")))
    print()
    print("Part 2:", part_2(*read_input("input.txt")))
    print()
    time_the_code(*read_input("input.txt"))
