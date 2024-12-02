def read_input(fname: str) -> list[int]:
    with open(fname) as file:
        return [x.strip() for x in file.readlines()]


def part_1(x):
    count = 0
    for xx in x:
        digits = [int(s) for s in list(xx) if s.isdigit()]
        count += 10*digits[0] + digits[-1]
    return count


def part_2(x):
    numbers = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }
    count = 0
    for y in x:
        digits = []
        for i in range(len(y)):
            # check if normal digit
            if y[i].isdigit():
                digits.append(int(y[i]))
                continue
            # check if a word digit
            for num in numbers:
                if num == y[i:i+len(num)]:
                    digits.append(numbers[num])
        count += 10*digits[0] + digits[-1]
    return count


if __name__ == "__main__":
    fname: str = "input.txt"
    inp = read_input(fname)
    print("Part 1:", part_1(inp))
    print("Part 2:", part_2(inp))
