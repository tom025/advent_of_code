import typing
from collections import defaultdict
from typing import Sequence

type Matrix[T] = Sequence[Sequence[T]]


def vectors[T](
    matrix: Matrix[T], group: typing.Callable[[int, int], int]
) -> Sequence[Sequence[T]]:
    groupings = defaultdict(list)
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            groupings[group(x, y)].append(matrix[y][x])
    return list(map(groupings.get, sorted(groupings)))


def match_word(word, chars: list[chr] | str) -> bool:
    w = list(word)
    cs = list(chars)
    return (w == cs) or (list(reversed(w)) == cs)


def count_matches(word: str, chars: list[chr] | str) -> int:
    return sum(
        1 if match_word(word, chars[idx : idx + len(word)]) else 0
        for idx in range(len(chars))
    )


def word_search(word, matrix):
    return sum(
        sum(count_matches(word, vector) for vector in vs)
        for vs in [
            vectors(matrix, lambda x, y: y),
            vectors(matrix, lambda x, y: x),
            vectors(matrix, lambda x, y: x + y),
            vectors(matrix, lambda x, y: x - y),
        ]
    )


def x_match(matrix, word):
    if len(matrix) < len(word) or len(matrix[0]) < len(word):
        return False
    f_diag = [matrix[i][i] for i in range(len(matrix))]
    b_diag = [matrix[i][len(matrix) - 1 - i] for i in range(len(matrix))]
    chars = list(word)
    r_chars = list(reversed(chars))
    return (f_diag == chars or f_diag == r_chars) and (
        b_diag == chars or b_diag == r_chars
    )


def x_word_search(matrix, word):
    return sum(
        1 if x_match(sub_matrix, word) else 0
        for sub_matrix in submatrices(matrix, len(word))
    )


def matrix_coords[T](
    matrix: Matrix[T],
) -> typing.Generator[tuple[int, int], None, None]:
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            yield x, y


def sub_slice[T](len_: int, i: int, sub_len: int) -> slice:
    half_len = sub_len // 2
    return slice(max(0, i - half_len), min(len_, i + half_len + 1))


def submatrices[T](matrix: Matrix[T], len_):
    return [
        [
            row[sub_slice(len(row), x, len_)]
            for row in matrix[sub_slice(len(matrix), y, len_)]
        ]
        for x, y in matrix_coords(matrix)
    ]


if __name__ == "__main__":
    with open("puzzle.txt", "r") as file:
        matrix = [list(l.rstrip()) for l in file]
        matches_count = word_search("XMAS", matrix)
        x_matches_count = x_word_search(matrix, "MAS")

        print(f"word_search: found XMAS {matches_count} times")
        print(f"x_word_search: found MAS {x_matches_count} times")
