import io
import textwrap

import pytest

from aoc_2025.day_04 import symbols, to_matrix, neighbours, solve, count_symbol, accessible_paper_rolls, \
    remove_paper_rolls


@pytest.fixture
def example_input():
    yield io.StringIO(textwrap.dedent("""\
    ..@@.@@@@.
    @@@.@.@.@@
    @@@@@.@.@@
    @.@@@@..@.
    @@.@@@@.@@
    .@@@@@@@.@
    .@.@.@.@@@
    @.@@@.@@@@
    .@@@@@@@@.
    @.@.@@@.@.
    """))

@pytest.fixture
def example_matrix(example_input):
    yield to_matrix(example_input)

def test_day04_example(example_input):
    s1, s2 = solve(example_input)
    assert s1 == 13
    assert s2 == 43


def test_to_matrix(example_input):
    assert to_matrix(example_input) == [
        list('..@@.@@@@.'),
        list('@@@.@.@.@@'),
        list('@@@@@.@.@@'),
        list('@.@@@@..@.'),
        list('@@.@@@@.@@'),
        list('.@@@@@@@.@'),
        list('.@.@.@.@@@'),
        list('@.@@@.@@@@'),
        list('.@@@@@@@@.'),
        list('@.@.@@@.@.'),
    ]

@pytest.mark.parametrize(
    'point, expected',
    [
        ((0, 0), [['.'], ['@', '@']]),
        ((9, 0), [['@'], ['@', '@']]),
        ((0, 9), [['.', '@'], ['.']]),
        ((9, 9), [['@', '.'], ['@']]),
        ((4, 4), [['@', '@', '@'], ['@', '@'], ['@', '@', '@']]),
    ],
)
def test_neighbours(example_matrix, point, expected):
    assert neighbours(example_matrix, point) == expected


@pytest.mark.parametrize(
    'example_neighbours, expected',
    [
        ([['.'], ['@', '@']], 2),
        ([['@'], ['@', '@']], 3),
        ([['.', '@'], ['.']], 1),
        ([['@', '.'], ['@']], 2),
        ([['@', '@', '@'], ['@', '@'], ['@', '@', '@']], 8),
    ],
)
def test_count_paper_rolls(example_neighbours: list[list[symbols]], expected):
    assert count_symbol(example_neighbours, '@') == expected


def test_remove_paper_rolls(example_matrix):
    assert remove_paper_rolls(example_matrix, accessible_paper_rolls(example_matrix)) == to_matrix(io.StringIO(textwrap.dedent("""\
    .......@..
    .@@.@.@.@@
    @@@@@...@@
    @.@@@@..@.
    .@.@@@@.@.
    .@@@@@@@.@
    .@.@.@.@@@
    ..@@@.@@@@
    .@@@@@@@@.
    ....@@@...
    """)))
