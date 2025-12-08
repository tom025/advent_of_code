import io
import textwrap

import pytest

from aoc_2025.day_07 import splitters_on_row, solve, parse_diagram, new_beams

@pytest.fixture
def example_diagram():
    yield io.StringIO(textwrap.dedent("""\
    .......S.......
    ...............
    .......^.......
    ...............
    ......^.^......
    ...............
    .....^.^.^.....
    ...............
    ....^.^...^....
    ...............
    ...^.^...^.^...
    ...............
    ..^...^.....^..
    ...............
    .^.^.^.^.^...^.
    ...............
    """))


@pytest.mark.parametrize(
    "i, expected",
    [
        (1, set()),
        (2, {7}),
        (4, {6, 8}),
    ]
)
def test_splitters_on_row(example_diagram, i, expected):
    _, splitters, *_ = parse_diagram(example_diagram)
    assert splitters_on_row(splitters, i) == expected


def test_day07_example(example_diagram):
    s1, s2 = solve(example_diagram)
    assert s1 == 21
    assert s2 == 40


def test_parse_diagram(example_diagram):
    source_location, splitter_locations, width, height = parse_diagram(example_diagram)
    assert width == 15
    assert height == 16
    assert source_location == (7, 0)
    assert splitter_locations == {
        (1, 14),
        (2, 12),
        (3, 10),
        (3, 14),
        (4, 8),
        (5, 6),
        (5, 10),
        (5, 14),
        (6, 4),
        (6, 8),
        (6, 12),
        (7, 2),
        (7, 6),
        (7, 14),
        (8, 4),
        (9, 6),
        (9, 10),
        (9, 14),
        (10, 8),
        (11, 10),
        (12, 12),
        (13, 14)
    }


@pytest.mark.parametrize(
    "beams, splitters, expected_new_beams, expected_splitters_hit",
    [
        ({7: 1}, set(), {7: 1}, set()),
        ({7: 1}, {6, 8}, {7: 1}, set()),
        ({7: 1}, {7}, {6: 1, 8: 1}, {7}),
        ({5: 1, 7: 1, 9: 1}, {5, 7, 9}, {4: 1, 6: 2, 8: 2, 10: 1}, {5, 7, 9}),
        ({5: 1, 7: 2, 9: 1}, {5, 7, 9}, {4: 1, 6: 3, 8: 3, 10: 1}, {5, 7, 9}),
        ({4: 1, 6: 1, 8: 1, 10: 1}, {4, 6, 10}, {3: 1, 5: 2, 7: 1, 8: 1, 9: 1, 11: 1}, {4, 6, 10}),
    ]
)
def test_new_beams(beams, splitters, expected_new_beams, expected_splitters_hit):
    assert new_beams(beams, splitters) == (expected_new_beams, expected_splitters_hit)