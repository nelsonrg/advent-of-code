from typing import NamedTuple
from functools import cmp_to_key


class PageOrderRule(NamedTuple):
    before: int
    after: int


def read_input(file_name: str) -> tuple[list[PageOrderRule], list[list[int]]]:
    with open(file_name) as f:
        all_data: list[str] = [line.strip() for line in f.readlines()]
    split_idx: int = all_data.index("")
    ordering_rules: list[PageOrderRule] = [
        PageOrderRule(*tuple(int(page) for page in rule.split("|")))
        for rule in all_data[:split_idx]
    ]
    updates: list[list[int]] = [
        [int(page) for page in update.split(",")]
        for update in all_data[split_idx+1:]
    ]
    return ordering_rules, updates


def part_1(ordering_rules: list[PageOrderRule], updates: [list[int]]) -> int:
    return sum(get_middle_page(update) for update in updates
               if is_in_correct_order(update, ordering_rules))


def is_in_correct_order(
        update: list[int], ordering_rules: list[PageOrderRule]
) -> bool:
    for i in range(len(update)):
        page: int = update[i]
        later_pages: list[int] = update[i+1:]
        for later_page in later_pages:
            rule = PageOrderRule(before=later_page, after=page)
            if rule in ordering_rules:
                return False
    return True


def get_middle_page(update: list[int]) -> int:
    assert len(update) % 2 == 1, "Number of pages is not odd."
    return update[(len(update) - 1) // 2]


def part_2(ordering_rules: list[PageOrderRule], updates: [list[int]]) -> int:
    return sum(get_middle_page(sort_update(update, ordering_rules))
               for update in updates
               if not is_in_correct_order(update, ordering_rules))


def sort_update(
        update: list[int], ordering_rules: list[PageOrderRule]
) -> list[int]:
    def compare_pages(page_0, page_1):
        if PageOrderRule(before=page_0, after=page_1) in ordering_rules:
            return -1
        elif PageOrderRule(before=page_1, after=page_0) in ordering_rules:
            return 1
        else:
            assert False, "No rule found"
    return sorted(update, key=cmp_to_key(compare_pages))


if __name__ == "__main__":
    ordering_rules, updates = read_input("day_5_input.txt")
    print(part_1(ordering_rules, updates))
    print(part_2(ordering_rules, updates))
