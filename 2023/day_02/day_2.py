def read_input(fname):
    result = {}
    with open(fname) as file:
        for line in file.readlines():
            game, sets = line.split(":")
            game = int(game.split()[-1])
            sets = sets.split(";")
            result[game] = []
            for s in sets:
                draws = s.split(",")
                s_dict = {}
                for draw in draws:
                    n = int(draw.split()[0])
                    if "blue" in draw:
                        c = "blue"
                    elif "red" in draw:
                        c = "red"
                    elif "green" in draw:
                        c = "green"
                    s_dict[c] = n
                result[game].append(s_dict)
    return result


def part_1(games):
    n_red = 12
    n_green = 13
    n_blue = 14

    counter = 0

    for game_number, game in games.items():
        is_possible = True
        for s in game:
            red_count = s.get("red", 0)
            green_count = s.get("green", 0)
            blue_count = s.get("blue", 0)
            if red_count > n_red or green_count > n_green or blue_count > n_blue:
                is_possible = False
                break
        if is_possible:
            counter += game_number
    return counter


def part_2(games):
    counter = 0
    for game_number, game in games.items():
        n_red = []
        n_green = []
        n_blue = []
        for s in game:
            n_red.append(s.get("red", 0))
            n_green.append(s.get("green", 0))
            n_blue.append(s.get("blue", 0))
        power = max(n_red)*max(n_green)*max(n_blue)
        counter += power
    return counter


if __name__ == "__main__":
    print("Test Part 1", part_1(read_input("test1.txt")))
    print("Part 1", part_1(read_input("input.txt")))
    print("Test Part 2", part_2(read_input("test1.txt")))
    print("Part 2", part_2(read_input("input.txt")))
