import collections
import itertools
import typing

Point = tuple[int, int]


def parse_tile_locations(
    textio: typing.TextIO,
) -> collections.abc.Generator[Point, None, None]:
    for line in textio:
        yield typing.cast(Point, tuple(int(i) for i in line.strip().split(",")))


def area(p1: Point, p2: Point) -> int:
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)


def find_max_area(
    tile_locations: collections.abc.Iterable[Point],
) -> tuple[tuple[Point, Point], int]:
    return sorted(
        ((pair, area(*pair)) for pair in itertools.combinations(tile_locations, 2)),
        key=lambda item: item[1],
        reverse=True,
    )[0]


def solve(example_input) -> tuple[int, int]:
    _, max_area = find_max_area(parse_tile_locations(example_input))
    return max_area, 0


if __name__ == "__main__":
    with open("input.txt") as f:
        s1, _ = solve(f)

    print(f"s1: {s1!r}")
