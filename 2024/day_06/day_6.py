from typing import NamedTuple
from copy import deepcopy


class Location(NamedTuple):
    row: int
    column: int


class Direction(NamedTuple):
    row: int
    column: int


def read_input(file_name: str) -> list[list[str]]:
    with open(file_name) as f:
        return [list(line.strip()) for line in f.readlines()]


def part_1(guard_map):
    return len(get_visited_locations(guard_map))


def get_visited_locations(guard_map) -> set[Location]:
    visited = set()
    location = get_symbol_location(guard_map, "^")
    direction = Direction(row=-1, column=0)
    while is_in_map(location, guard_map):
        visited.add(location)
        location, direction = get_next_location(location, direction, guard_map)
    return visited


def is_in_map(location: Location, guard_map: list[list[str]]) -> bool:
    max_row: int = len(guard_map)
    max_col: int = len(guard_map[0])
    if not location:
        return False
    return (0 <= location.row < max_row) and (0 <= location.column < max_col)


def get_symbol_location(guard_map: list[list[str]], symbol: str) -> Location:
    for i, row in enumerate(guard_map):
        if symbol in row:
            return Location(row=i, column=row.index(symbol))
    return None


def get_next_location(location: Location, direction: Direction, guard_map: list[list[str]]) -> tuple[Location, Direction]:
    next_location, next_direction = move_forward(location, direction)
    if is_blocked(next_location, guard_map):
        return rotate(location, direction)
    return next_location, next_direction


def move_forward(location: Location, direction: Direction) -> tuple[Location, Direction]:
    return Location(location.row + direction.row, location.column + direction.column), direction


def rotate(location: Location, direction: Direction) -> tuple[Location, Direction]:
    R = [[0, 1],
         [-1, 0]]
    new_direction = Direction(
        row=direction.row * R[0][0] + direction.column * R[0][1],
        column=direction.row * R[1][0] + direction.column * R[1][1]
    )
    return location, new_direction


def is_blocked(location: Location, guard_map: list[list[str]]) -> bool:
    if not is_in_map(location, guard_map):
        return False
    return guard_map[location.row][location.column] == "#"


def part_2(guard_map: list[list[str]]) -> int:
    total: int = 0
    possible_locations = get_visited_locations(guard_map)

    for location in possible_locations:
        if guard_map[location.row][location.column] == ".":
            m = deepcopy(guard_map)
            m[location.row][location.column] = "#"
            total += is_loop(m)
            
    return total


def is_loop(guard_map: list[list[str]]) -> bool:
    visited = set()
    location = get_symbol_location(guard_map, "^")
    direction = Direction(row=-1, column=0)
    while is_in_map(location, guard_map):
        if (location, direction) in visited:
            return True
        visited.add((location, direction))
        location, direction = get_next_location(location, direction, guard_map)
    return False


if __name__ == "__main__":
    guard_map = read_input("day_6_input.txt")
    print(part_1(guard_map))
    print(part_2(guard_map))
