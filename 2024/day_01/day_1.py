def read_input(file_name):
    with open(file_name) as f:
        list_1, list_2 = zip(*[line.split() for line in f.readlines()])
    list_1 = [int(x) for x in list_1]
    list_2 = [int(x) for x in list_2]
    return list_1, list_2


def part_1(list_1, list_2):
    sorted_list_1 = sorted(list_1)
    sorted_list_2 = sorted(list_2)
    return sum(
        map(
            lambda x: abs(x[0] - x[1]),
            zip(sorted_list_1, sorted_list_2)
        )
    )


def part_2(list_1, list_2):
    return sum(
        map(
            lambda x: x * list_2.count(x),
            list_1
        )
    )


if __name__ == "__main__":
    inp = read_input("day_1_input.txt")
    print(part_1(*inp))
    print(part_2(*inp))
