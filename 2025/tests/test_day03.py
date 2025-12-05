import io
import textwrap

import pytest

from aoc_2025.day_03 import to_joltages, solve, parse_banks, max_joltage, max_joltages


@pytest.fixture
def example_input():
    yield io.StringIO(textwrap.dedent("""\
    987654321111111
    811111111111119
    234234234234278
    818181911112111
    """))


@pytest.fixture
def example_banks():
    yield [
        to_joltages('987654321111111'),
        to_joltages('811111111111119'),
        to_joltages('234234234234278'),
        to_joltages('818181911112111')
    ]


def test_day03_example(example_input):
    solution = solve(example_input)
    assert solution == 357


def test_parse_banks(example_input, example_banks):
    assert list(parse_banks(example_input)) == example_banks


@pytest.mark.parametrize(
    "bank, batteries_allowed, expected",
    [
        (to_joltages('987654321111111'), 2, 98),
        (to_joltages('811111111111119'), 2, 89),
        (to_joltages('234234234234278'), 2, 78),
        (to_joltages('818181911112111'), 2, 92),
    ]
)
def test_max_joltage(bank, batteries_allowed, expected):
    assert max_joltage(bank, batteries_allowed=batteries_allowed) == expected


def test_max_joltages(example_banks):
    assert list(max_joltages(iter(example_banks))) == [
        98,
        89,
        78,
        92
    ]
