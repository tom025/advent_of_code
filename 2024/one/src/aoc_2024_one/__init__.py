import itertools
import pathlib
import os
import typing
from typing import Generator, Iterator, Iterable


def to_lines(content: typing.TextIO) -> Generator[str, None, None]:
    for line in content:
        yield line.rstrip()


def parse_line(l: str) -> (int, int):
    left, right = l.split("   ")
    return int(left), int(right)


def to_left_right(parsed_lines: Iterator[tuple[int, int]]) -> Iterator[Iterable[int]]:
    return zip(*parsed_lines)


def sort_lists(lists: Iterator[Iterable[int]]) -> Iterator[Iterable[int]]:
    for l in lists:
        yield sorted(l)


def calculate_distances(locations: Iterator[tuple[int, int]]) -> Iterator[int]:
    for l, r in locations:
        yield abs(l - r)


def total_distance(locations: Iterator[Iterable[int]]) -> int:
    return sum(calculate_distances(zip(*sort_lists(locations))))


def similarity_score(location_lists: Iterator[Iterable[int]]) -> int:
    left, right = location_lists
    duplicate_counts = {
        l: len(list(dups)) for l, dups in itertools.groupby(sorted(right))
    }
    return sum(l * duplicate_counts.get(l, 0) for l in left)


def extract_location_lists(content: typing.TextIO) -> Iterator[Iterable[int]]:
    return to_left_right(parse_line(line) for line in to_lines(content))


def calculate_stats(path: os.PathLike | str) -> dict[str, int]:
    with open(path, "r") as f:
        lists_1, lists_2 = itertools.tee(extract_location_lists(f))
        return {
            "total_distance": total_distance(lists_1),
            "similarity_score": similarity_score(lists_2),
        }


if __name__ == "__main__":
    stats = calculate_stats(pathlib.Path("lists.txt"))
    print(f"total_distance: {stats['total_distance']}")
    print(f"similarity_score: {stats['similarity_score']}")
