import io
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


def calculate_total_distance_from(content: typing.TextIO) -> int:
    return sum(
        calculate_distances(
            zip(
                *sort_lists(
                    to_left_right(parse_line(line) for line in to_lines(content))
                )
            )
        )
    )


def total_distance(path: os.PathLike | str) -> int:
    with open(path, "r") as f:
        return calculate_total_distance_from(f)


if __name__ == "__main__":
    print(f"total_distance: {total_distance(pathlib.Path('lists.txt'))}")
