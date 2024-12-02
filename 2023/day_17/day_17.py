import numpy as np
from queue import PriorityQueue


DIRECTIONS = {(1, 0), (0, 1), (-1, 0), (0, -1)}


def read_input(fname):
    result = []
    with open(fname) as file:
        for line in file.readlines():
            costs = [int(x) for x in line.strip()]
            result.append(costs)
    return np.array(result)


def custom_dijkstra(grid, source, end, minimum, maximum):
    heat = 0
    pqueue = PriorityQueue()
    pqueue.put((0, source, (0, 0)))
    seen = set()
    # we will build the graph from the grid as we go
    while pqueue:
        heat, loc, prev_direction = pqueue.get()  # best vertex
        # end condition
        if loc == end:
            return heat
        # don't revisit node/direction pairs
        if (loc, prev_direction) in seen:
            continue
        seen.add((loc, prev_direction))
        # visit each neighbor
        # do not go the same direction or backwards
        for dx, dy in DIRECTIONS - {prev_direction, tuple(-d for d in prev_direction)}:
            x, y = loc
            h = heat
            for i in range(maximum):
                x, y = x+dx, y+dy
                if (x, y) in grid:
                    h += grid[(x, y)]
                    if i >= minimum-1:
                        pqueue.put((h, (x, y), (dx, dy)))


def part_1(x):
    y = {(i, j): x[i, j] for i in range(x.shape[0]) for j in range(x.shape[1])}
    return custom_dijkstra(y, (0, 0), (x.shape[0]-1, x.shape[1]-1), 1, 3)


def part_2(x):
    y = {(i, j): x[i, j] for i in range(x.shape[0]) for j in range(x.shape[1])}
    return custom_dijkstra(y, (0, 0), (x.shape[0]-1, x.shape[1]-1), 4, 10)


if __name__ == "__main__":
    print("Part 1 test:", part_1(read_input("test.txt")))
    print("Part 1:", part_1(read_input("input.txt")))
    print()
    print("Part 2 test:", part_2(read_input("test.txt")))
    print("Part 2:", part_2(read_input("input.txt")))
