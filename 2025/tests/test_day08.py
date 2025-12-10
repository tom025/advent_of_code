import io
import textwrap

import pytest

from aoc_2025.day_08 import (
    parse_input,
    distance,
    find_all_distances,
    solve,
    Connection,
    collect_circuits,
)


@pytest.fixture
def example_input():
    yield io.StringIO(
        textwrap.dedent(
            """\
            162,817,812
            57,618,57
            906,360,560
            592,479,940
            352,342,300
            466,668,158
            542,29,236
            431,825,988
            739,650,466
            52,470,668
            216,146,977
            819,987,18
            117,168,530
            805,96,715
            346,949,466
            970,615,88
            941,993,340
            862,61,35
            984,92,344
            425,690,689
    """
        )
    )


def test_day08_example(example_input):
    s1, _ = solve(example_input, total_connections=10)
    assert s1 == 40


def test_parse_j_box_coords(example_input):
    parsed = parse_input(example_input)

    assert (162, 817, 812) in parsed
    assert (216, 146, 977) in parsed
    assert (425, 690, 689) in parsed


@pytest.mark.parametrize(
    "p1, p2, expected", [((62, 817, 812), (216, 146, 977), 707.9420880269798)]
)
def test_distance(p1, p2, expected):
    assert distance(p1, p2) == expected


def test_find_all_distances(example_input):
    ds = find_all_distances(parse_input(example_input))
    assert len(ds) == 190
    assert (
        next(
            d
            for c, d in ds
            if c == Connection.from_points((216, 146, 977), (162, 817, 812))
        )
        == 693.0959529531247
    )

    assert ds[0][0] == Connection.from_points((425, 690, 689), (162, 817, 812))
    assert ds[1][0] == Connection.from_points((431, 825, 988), (162, 817, 812))


def test_collect_shortest_circuits(example_input):
    ds = find_all_distances(parse_input(example_input))

    circuits, final_connection = collect_circuits(ds, 10)

    assert final_connection is None
    assert {(425, 690, 689), (162, 817, 812), (431, 825, 988)} <= circuits[0]

    assert len(circuits) == 4
    largets_circuits = sorted(circuits, key=len, reverse=True)
    assert len(largets_circuits[0]) == 5
    assert len(largets_circuits[1]) == 4
    assert len(largets_circuits[2]) == 2
    assert len(largets_circuits[3]) == 2


def test_collect_shortest_circuits_until_all_connected(example_input):
    ds = find_all_distances(parse_input(example_input))

    circuits, final_connection = collect_circuits(ds, len(ds))

    assert len(circuits) == 1
    assert len(circuits[0]) == 20
    assert final_connection == Connection.from_points((216, 146, 977), (117, 168, 530))
