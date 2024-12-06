from typing import NamedTuple


SYMBOLS = ("^", ">", "v", "<")


class Location(NamedTuple):
    row: int
    column: int


def read_input(file_name: str) -> list[list[str]]:
    with open(file_name) as f:
        return [list(line.strip()) for line in f.readlines()]


def part_1(guard_map):
    visited = set()
    location, _ = get_symbol_location(guard_map)
    while is_in_map(location, guard_map):
        visited.add(location)
        step(guard_map)
        location, _ = get_symbol_location(guard_map)
    return len(visited)


def is_in_map(location: Location, guard_map: list[list[str]]) -> bool:
    max_row: int = len(guard_map)
    max_col: int = len(guard_map[0])
    if not location:
        return False
    return (0 <= location.row < max_row) and (0 <= location.column < max_col)


def get_symbol_location(guard_map: list[list[str]]) -> tuple[Location, str]:
    for idx, row in enumerate(guard_map):
        for symbol in SYMBOLS:
            if symbol in row:
                return Location(row=idx, column=row.index(symbol)), symbol
    return None, None


def step(guard_map: list[list[str]]) -> None:
    location, symbol = get_symbol_location(guard_map)
    new_location, new_symbol = get_next_location(symbol, location, guard_map)
    guard_map[location.row][location.column] = "."
    if is_in_map(new_location, guard_map):
        guard_map[new_location.row][new_location.column] = new_symbol


def get_next_location(symbol, location, guard_map):
    next_location, next_symbol = move_forward(symbol, location)
    if is_blocked(next_location, guard_map):
        return rotate(symbol, location)
    return next_location, next_symbol


def move_forward(symbol: str, current_location: Location) -> tuple[Location, str]:
    next_location = {
        "^": (-1, 0),
        "v": (1, 0),
        ">": (0, 1),
        "<": (0, -1)
    }
    return (
        Location(*tuple(sum(x) for x in zip(next_location[symbol], current_location))),
        symbol
    )


def rotate(symbol, current_location):
    next_symbol = {
        "^": ">",
        "v": "<",
        ">": "v",
        "<": "^"
    }
    return move_forward(next_symbol[symbol], current_location)


def is_blocked(location, guard_map):
    if not is_in_map(location, guard_map):
        return False
    return guard_map[location.row][location.column] == "#"


if __name__ == "__main__":
    guard_map = read_input("day_6_input.txt")
    print(part_1(guard_map))
