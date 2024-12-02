from queue import Queue
from functools import reduce
from math import lcm


def read_input(fname):
    modules = {}
    broadcaster = None
    with open(fname) as file:
        for line in file.readlines():
            x = line.strip()
            inp, out = x.split(" -> ")
            if inp == "broadcaster":
                broadcaster = [o.strip() for o in out.split(",")]
            else:
                op = inp[0]
                inp = inp[1:]
                out = [o.strip() for o in out.split(",")]
                modules[inp] = {"operator": op,
                                "output": out}
    for k, v in modules.items():
        if v["operator"] == "%":
            v["state"] = 0
        elif v["operator"] == "&":
            v["state"] = {k2: 0 for k2, v2 in modules.items() if k in v2["output"]}
    return broadcaster, modules


def send_pulse(source, destination, pulse, modules):
    if destination not in modules:
        return None

    x = modules[destination]
    if x["operator"] == "%":
        if pulse == 0:
            x["state"] = int(not x["state"])
            return x["state"]
        else:
            return None
    elif x["operator"] == "&":
        x["state"][source] = pulse
        return int(not (reduce(lambda x, y: x & y, x["state"].values())))


def part_1_helper(broadcaster, modules):
    counter = 0
    total = 1
    q = Queue()
    for destination in broadcaster:
        q.put((None, destination, 0))
    while not q.empty():
        source, destination, pulse = q.get()
        total += 1
        counter += pulse
        p = send_pulse(source, destination, pulse, modules)
        if p is None:
            continue
        for out in modules[destination]["output"]:
            q.put((destination, out, p))
    return counter, total-counter


def part_1(broadcaster, modules):
    results = [part_1_helper(broadcaster, modules) for _ in range(1000)]
    high, low = zip(*results)
    print(sum(high), sum(low))
    return sum(high)*sum(low)


def part_2_helper(broadcaster, modules, end):
    end_source = None
    counter = 0
    total = 1
    q = Queue()
    for destination in broadcaster:
        q.put((None, destination, 0))
    while not q.empty():
        source, destination, pulse = q.get()
        total += 1
        counter += pulse
        p = send_pulse(source, destination, pulse, modules)
        if destination == end and pulse == 1:
            end_source = source
        if p is None:
            continue
        for out in modules[destination]["output"]:
            q.put((destination, out, p))
    return end_source


def part_2(broadcaster, modules):
    m = 5000
    c = 0
    s = {k: 0 for k in modules if "dt" in modules[k]["output"]}
    while any([x == 0 for x in s.values()]):
        c += 1
        source = part_2_helper(broadcaster, modules, "dt")
        if source is not None:
            s[source] = c
        if c > m:
            break
    print(c)
    print(s)
    return lcm(*s.values())


if __name__ == "__main__":
    print("Part 1 test 1:", part_1(*read_input("test1.txt")))
    print("Part 1 test 2:", part_1(*read_input("test2.txt")))
    print("Part 1:", part_1(*read_input("input.txt")))
    print()
    print("Part 2:", part_2(*read_input("input.txt")))
