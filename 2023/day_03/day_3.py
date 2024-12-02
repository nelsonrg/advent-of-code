import re


def read_input(fname):
    symbol_locations = []
    numbers = []
    row = 0
    with open(fname) as file:
        for line in file.readlines():
            line = line.strip()
            numbers += \
                [(int(line[m.start(0):m.end(0)]), row, m.start(0), m.end(0)-1)
                 for m in re.finditer(r"(\d+)", line)]
            for col, x in enumerate(line):
                if not x.isdigit() and x != ".":
                    symbol_locations.append((row, col))
            row += 1
    return symbol_locations, numbers


def read_input2(fname):
    symbol_locations = {}
    numbers = []
    row = 0
    with open(fname) as file:
        for line in file.readlines():
            line = line.strip()
            numbers += \
                [(int(line[m.start(0):m.end(0)]), row, m.start(0), m.end(0)-1)
                 for m in re.finditer(r"(\d+)", line)]
            for col, x in enumerate(line):
                if not x.isdigit() and x != ".":
                    v = (row, col)
                    if x not in symbol_locations:
                        symbol_locations[x] = [v]
                    else:
                        symbol_locations[x].append(v)
            row += 1
    return symbol_locations, numbers


def part_1(symbol_locations, numbers):
    count = 0
    for n, r, i, j in numbers:
        for x in range(i, j+1):
            if (r-1, x) in symbol_locations:
                count += n
                break
            if (r-1, x-1) in symbol_locations:
                count += n
                break
            if (r-1, x+1) in symbol_locations:
                count += n
                break
            if (r+1, x) in symbol_locations:
                count += n
                break
            if (r+1, x-1) in symbol_locations:
                count += n
                break
            if (r+1, x+1) in symbol_locations:
                count += n
                break
            if (r, x-1) in symbol_locations:
                count += n
                break
            if (r, x+1) in symbol_locations:
                count += n
                break
    return count


def part_2(symbol_locations, numbers):
    symbol_locations = symbol_locations["*"]
    count = 0

    number_locations = [(x[1], y) for x in numbers for y in range(x[2], x[3]+1)]
    number_locations_set = set(number_locations)
    number_values = [(i, x[0]) for i, x in enumerate(numbers)
                     for y in range(x[2], x[3]+1)]

    for r, c in symbol_locations:
        search_offset = [(r-1, c-1), (r-1, c), (r-1, c+1),
                         (r, c-1), (r, c+1),
                         (r+1, c-1), (r+1, c), (r+1, c+1)]
        neighbors_idx = []
        neighbors_value = []
        for s in search_offset:
            if s in number_locations_set:
                i, v = number_values[number_locations.index(s)]
                if i not in neighbors_idx:
                    neighbors_idx.append(i)
                    neighbors_value.append(v)
        if len(neighbors_value) == 2:
            count += neighbors_value[0]*neighbors_value[1]
    return count


if __name__ == "__main__":
    print("Test Part 1", part_1(*read_input("test.txt")))
    print("Part 1", part_1(*read_input("input.txt")))
    print("Test Part 2", part_2(*read_input2("test.txt")))
    print("Part 2", part_2(*read_input2("input.txt")))
