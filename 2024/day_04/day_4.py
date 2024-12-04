import functools


def read_input(file_name):
    with open(file_name) as f:
        return tuple(line.strip() for line in f.readlines())


def part_1(word_search):
    max_row = len(word_search)
    max_col = len(word_search[0])
    total_matches = 0
    for row in range(0, max_row):
        for col in range(0, max_col):
            total_matches += search_word(word_search, row, col, "XMAS")
    return total_matches


def search_word(word_search, row, col, word):
    max_row = len(word_search)
    max_col = len(word_search[0])
    row_idx = [[row] * len(word)]
    col_idx = [[col] * len(word)]
    n_matches = 0
    if row >= len(word) - 1:
        row_idx.append([row - delta for delta in range(0, len(word))])
    if row + len(word) <= max_row:
        row_idx.append([row + delta for delta in range(0, len(word))])
    if col >= len(word) - 1:
        col_idx.append([col - delta for delta in range(0, len(word))])
    if col + len(word) <= max_col:
        col_idx.append([col + delta for delta in range(0, len(word))])
    for ridx in row_idx:
        for cidx in col_idx:
            if "".join([word_search[r][c] for r, c in zip(ridx, cidx)]) == word:
                n_matches += 1
    return n_matches


def part_2(word_search):
    max_row = len(word_search)
    max_col = len(word_search[0])
    total_matches = 0
    for row in range(0, max_row):
        for col in range(0, max_col):
            total_matches += search_word_x(word_search, row, col, "MAS")
    return total_matches


def search_word_x(word_search, row, col, word):
    max_row = len(word_search)
    max_col = len(word_search[0])
    # don't search if it can't fit
    if (row + len(word) > max_row) or (col + len(word) > max_col):
        return False
    diag_left_right = "".join([word_search[row + delta][col + delta] for delta in range(0, len(word))])
    diag_right_left = "".join([word_search[row + delta][col + len(word) - 1 - delta] for delta in range(0, len(word))])
    words = [word, word[::-1]]
    return (diag_left_right in words) and (diag_right_left in words)


@functools.cache
def search_word_flexible(word_search, row, col, word, word_so_far):
    """
    Oops, I misread the problem initially and thought that the word search could move either direction at each letter.
    """
    word_so_far = word_so_far + word_search[row][col]
    if word_so_far != word[0:len(word_so_far)]:
        return 0
    if word_so_far == word:
        return 1
    max_row = len(word_search)
    max_col = len(word_search[0])
    legal_moves = [(row + delta_row, col + delta_col) for delta_col in range(-1, 2) for delta_row in range(-1, 2)
                   if (0 <= row + delta_row < max_row) and (0 <= col + delta_col < max_col) and (delta_row + delta_col != 0)]
    n_found = 0
    for new_row, new_col in legal_moves:
        n_found += search_word(word_search, new_row, new_col, word, word_so_far)
    return n_found


if __name__ == "__main__":
    inp = read_input("day_4_input.txt")
    print(part_1(inp))
    print(part_2(inp))