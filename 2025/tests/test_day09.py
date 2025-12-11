import io
import textwrap

import pytest

from aoc_2025.day_09 import parse_tile_locations, area, find_max_area, solve


@pytest.fixture
def example_input():
    yield io.StringIO(
        textwrap.dedent(
            """\
            7,1
            11,1
            11,7
            9,7
            9,5
            2,5
            2,3
            7,3
            """
        )
    )


def text_day09_example(example_input):
    s1, _ = solve(example_input)
    assert s1 == 50


@pytest.mark.parametrize(
    "p1,p2,expected",
    [
        ((2, 5), (9, 7), 24),
        ((7, 1), (11, 7), 35),
        ((7, 3), (2, 3), 6),
        ((2, 5), (11, 1), 50),
    ],
)
def test_area(p1, p2, expected):
    assert area(p1, p2) == expected


def test_parse_tile_locations(example_input):
    tile_locs = list(parse_tile_locations(example_input))
    assert len(tile_locs) == 8
    assert (7, 1) in tile_locs
    assert (9, 5) in tile_locs
    assert (7, 3) in tile_locs


def test_find_max_area(example_input):
    tiles, max_area = find_max_area(parse_tile_locations(example_input))

    assert len(tiles) == 2
    assert (2, 5) in tiles
    assert (11, 1) in tiles
    assert max_area == 50
