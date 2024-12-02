def read_input(fname):
    result = {}
    name = ""
    value_list = []
    with open(fname) as file:
        for line in file.readlines():
            if "seeds:" in line:
                result["seeds"] = [int(x) for x in line.split(":")[-1].split()]
            elif "map" in line:
                result[name] = value_list
                name = line.split()[0]
                value_list = []
            else:
                y = [int(x) for x in line.split()]
                if len(y) > 0:
                    value_list.append([int(x) for x in line.split()])
    result[name] = value_list
    return result


class Mapper:
    def __init__(self, inp):
        self.values = inp
        self.in_ranges = [range(x[1], x[1]+x[2]) for x in self.values]

    def get(self, x):
        for i, r in enumerate(self.in_ranges):
            if x in r:
                v = self.values[i]
                return x - v[1] + v[0]
        return x


def part_1(x):
    seeds = x["seeds"]

    order = ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water",
             "water-to-light", "light-to-temperature", "temperature-to-humidity",
             "humidity-to-location"]

    previous = seeds
    for y in order:
        m = Mapper(x[y])
        previous = [m.get(s) for s in previous]

    return min(previous)


def part_2_mapping(input_ranges, map_ranges):
    result = []
    while input_ranges:
        input_range = input_ranges.pop()
        converted = False
        for map_range, conversion in map_ranges:
            # convert whole range
            if (input_range.start in map_range) and (input_range.stop-1 in map_range):
                result.append(
                    range(input_range.start+conversion, input_range.stop+conversion)
                )
                converted = True
                break
            # only first part is in the map range
            elif input_range.start in map_range:
                result.append(
                    range(input_range.start+conversion, map_range.stop+conversion)
                )
                input_ranges.append(range(map_range.stop, input_range.stop))
                converted = True
                break
            # only last part is in map range
            elif input_range.stop-1 in map_range:
                result.append(
                    range(map_range.start+conversion, input_range.stop+conversion)
                )
                input_ranges.append(range(input_range.start, map_range.start))
                converted = True
                break
        # no overlap found
        if not converted:
            result.append(input_range)
    return result


def part_2(inp):
    seeds = inp["seeds"]
    order = ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water",
             "water-to-light", "light-to-temperature", "temperature-to-humidity",
             "humidity-to-location"]

    # build dict of ranges and conversions/offsets
    map_ranges = {}
    for step in order:
        map_ranges[step] = [(range(x[1], x[1]+x[2]), x[0]-x[1]) for x in inp[step]]

    # get seed ranges
    input_ranges = [range(x, x+y) for x, y in zip(seeds[::2], seeds[1::2])]
    for step in order:
        input_ranges = part_2_mapping(input_ranges, map_ranges[step])

    start_values = [x.start for x in input_ranges]
    print("\tNumber of intervals:", len(start_values))
    return min(start_values)


if __name__ == "__main__":
    print("Part 1 test:", part_1(read_input("test.txt")))
    print("Part 1:", part_1(read_input("input.txt")))
    print("Part 2 test:", part_2(read_input("test.txt")))
    print("Part 2:", part_2(read_input("input.txt")))
