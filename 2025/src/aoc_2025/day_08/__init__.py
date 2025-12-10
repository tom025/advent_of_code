import dataclasses
import itertools
import math
import operator
import typing

Point = tuple[int, int, int]


@dataclasses.dataclass(frozen=True)
class Connection:
    points: frozenset[Point]

    @classmethod
    def from_points(cls, p1: Point, p2: Point) -> "Connection":
        return cls(frozenset((p1, p2)))


def parse_input(textio: typing.TextIO) -> set[Point]:
    return set(
        typing.cast(Point, tuple(int(n) for n in line.strip().split(",")))
        for line in textio
    )


def distance(p1: Point, p2: Point) -> float:
    return math.sqrt(sum((p1[i] - p2[i]) ** 2 for i in range(3)))


def find_all_distances(
    coords: set[Point],
) -> list[tuple[Connection, float]]:
    return list(
        sorted(
            (
                (c, distance(*c.points))
                for c in (
                    Connection.from_points(p1, p2)
                    for p1, p2 in itertools.combinations(coords, 2)
                )
            ),
            key=lambda i: i[1],
        )
    )


def collect_circuits(
    distances: list[tuple[Connection, float]], total_connections: int
) -> list[set[Point]]:
    circuits: list[set[Point]] = []
    for i in range(total_connections):
        connection, _ = distances[i]
        c_points = connection.points
        connection_possibilities = list(
            circuit for circuit in circuits if c_points.intersection(circuit)
        )
        if any(c_points <= circuit for circuit in connection_possibilities):
            continue
        if len(connection_possibilities) == 0:
            circuits.append(set(c_points))
            continue

        first, *rest = connection_possibilities
        first.update(c_points)
        for c in rest:
            first.update(c)
            circuits.remove(c)

    return circuits


def solve(textio: typing.TextIO, total_connections: int) -> tuple[int, int]:
    distances = find_all_distances(parse_input(textio))
    *_, s1_ = itertools.accumulate(
        itertools.islice(
            (
                len(c)
                for c in sorted(
                    collect_circuits(distances, total_connections),
                    key=len,
                    reverse=True,
                )
            ),
            3,
        ),
        operator.mul,
        initial=1,
    )
    return s1_, 0


if __name__ == "__main__":
    with open("input.txt") as f:
        s1, _ = solve(f, total_connections=1000)

    print(f"s1: {s1!r}")
