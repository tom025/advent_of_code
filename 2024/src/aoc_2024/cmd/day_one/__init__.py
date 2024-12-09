import itertools
import os
import pathlib
from typing import Iterator, Iterable

from src.aoc_2024.io import read_file_lines


def parse_line(line: str) -> (int, int):
    left, right = line.split("   ")
    return int(left), int(right)


def to_left_right(parsed_lines: Iterator[tuple[int, int]]) -> Iterator[Iterable[int]]:
    return zip(*parsed_lines)


def sort_lists(lists: Iterator[Iterable[int]]) -> Iterator[Iterable[int]]:
    for list_ in lists:
        yield sorted(list_)


def calculate_distances(locations: Iterator[tuple[int, int]]) -> Iterator[int]:
    for left, right in locations:
        yield abs(left - right)


def total_distance(locations: Iterator[Iterable[int]]) -> int:
    return sum(calculate_distances(zip(*sort_lists(locations))))


def similarity_score(location_lists: Iterator[Iterable[int]]) -> int:
    left, right = location_lists
    duplicate_counts = {
        location: len(list(dups)) for location, dups in itertools.groupby(sorted(right))
    }
    return sum(location * duplicate_counts.get(location, 0) for location in left)


def extract_location_lists(lines: Iterator[str]) -> Iterator[Iterable[int]]:
    return to_left_right(parse_line(line) for line in lines)


def calculate_stats(path: os.PathLike | str) -> dict[str, int]:
    lists_1, lists_2 = itertools.tee(extract_location_lists(read_file_lines(path)))
    return {
        "total_distance": total_distance(lists_1),
        "similarity_score": similarity_score(lists_2),
    }


if __name__ == "__main__":
    stats = calculate_stats(pathlib.Path("lists.txt"))
    print(f"total_distance: {stats['total_distance']}")
    print(f"similarity_score: {stats['similarity_score']}")
