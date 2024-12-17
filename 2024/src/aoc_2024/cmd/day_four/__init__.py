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


if __name__ == "__main__":
    with open("puzzle.txt", "r") as file:
        matches_count = word_search("XMAS", [list(l.rstrip()) for l in file])
        print(f"found XMAS {matches_count} times")
