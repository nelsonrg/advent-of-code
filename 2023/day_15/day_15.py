from collections import OrderedDict


def read_input(fname):
    result = []
    with open(fname) as file:
        for line in file.readlines():
            springs = line.strip().split(",")
            result.append(springs)
    return result


class HolidayHashMap:
    def __init__(self):
        self.size = 256
        self.table = [OrderedDict() for _ in range(self.size)]

    @staticmethod
    def hash(x):
        h = 0
        for c in x:
            h = ((h + ord(c)) * 17) % 256
        return h

    def put(self, k, v):
        h = HolidayHashMap.hash(k)
        self.table[h][k] = v

    def get(self, k):
        h = HolidayHashMap.hash(k)
        return self.table[h][k]

    def delete(self, k):
        h = HolidayHashMap.hash(k)
        if k in self.table[h]:
            del self.table[h][k]

    def calculate_focusing_power(self):
        power = 0
        for i, box in enumerate(self.table):
            for j, v in enumerate(box.values()):
                power += (i + 1) * (j + 1) * v
        return power


def part_1(x):
    x = x[0]
    return sum(HolidayHashMap.hash(y) for y in x)


def part_2(x):
    x = x[0]
    hh_map = HolidayHashMap()
    for y in x:
        if "-" in y:
            key = y[:-1]
            hh_map.delete(key)
        elif "=" in y:
            key, value = y.split("=")
            value = int(value)
            hh_map.put(key, value)
        else:
            print("Error!", y)

    return hh_map.calculate_focusing_power()


if __name__ == "__main__":
    print("Part 1 test:", part_1(read_input("test.txt")))
    print("Part 1:", part_1(read_input("input.txt")))
    print()
    print("Part 2 test:", part_2(read_input("test.txt")))
    print("Part 2:", part_2(read_input("input.txt")))
