def process_entry(x):
    out = x.strip()
    out = x.split(":")
    card_number = out[0].split()[-1]
    out = out[1].split("|")
    winning_numbers = [int(n) for n in out[0].split()]
    numbers = [int(n) for n in out[1].split()]
    return card_number, winning_numbers, numbers


def read_input(fname):
    with open(fname) as file:
        return [process_entry(line) for line in file.readlines()]


def part_1(winning_numbers, drawn_numbers):
    score = 0
    for w, n in zip(winning_numbers, drawn_numbers):
        count = 0
        for x in n:
            if x in w:
                count += 1
        if count > 0:
            score += 2 ** (count - 1)
    return score


def part_2(card_number, winning_numbers, drawn_numbers):
    copies = [1]*len(card_number)
    for i, (w, n) in enumerate(zip(winning_numbers, drawn_numbers)):
        count = 0
        for x in n:
            if x in w:
                count += 1
        for j in range(i+1, i+1+count):
            copies[j] += copies[i]
    return sum(copies)


if __name__ == "__main__":
    card_number, winning_numbers, drawn_numbers = zip(*read_input("test.txt"))
    print("Part 1 test:", part_1(*list(zip(*read_input("test.txt")))[1:]))
    print("Part 1:", part_1(*list(zip(*read_input("input.txt")))[1:]))
    print("Part 2 test:", part_2(*list(zip(*read_input("test.txt")))))
    print("Part 2:", part_2(*list(zip(*read_input("input.txt")))))
