import io
import textwrap

import pytest

from aoc_2025.day_02 import solve, parse_ranges, parse_range, is_valid_product_id, find_invalid_product_ids, \
    invalid_product_ids_for_ranges, sum_invalid_product_ids


@pytest.fixture
def example_input():
    yield io.StringIO(textwrap.dedent("""\
    11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124\
    """))

@pytest.fixture
def example_ranges(example_input):
    yield parse_ranges(example_input)


@pytest.fixture
def example_invalid_product_ids(example_ranges):
    yield invalid_product_ids_for_ranges(example_ranges)

def test_day01_example(example_input):
    assert solve(example_input) == 1_227_775_554


def test_parse_ranges(example_input):
    parsed_ranges = list(parse_ranges(example_input))
    assert parsed_ranges == [
        range(11, 23),
        range(95, 116),
        range(998, 1013),
        range(1188511880, 1188511891),
        range(222220, 222225),
        range(1698522, 1698529),
        range(446443, 446450),
        range(38593856, 38593863),
        range(565653, 565660),
        range(824824821, 824824828),
        range(2121212118, 2121212125)
    ]


@pytest.mark.parametrize(
    "id, expected",
    [
        (55, False),
        (6464, False),
        (123123, False),
        (101, True)
    ]
)
def test_is_valid_product_id(id, expected):
    assert is_valid_product_id(id) == expected


@pytest.mark.parametrize(
    'example_range, expected',
    [
        (parse_range('11-22'), [11, 22]),
        (parse_range('95-115'), [99]),
        (parse_range('1698522-1698528'), [])
    ]
)
def test_find_invalid_product_ids(example_range: range, expected):
    assert find_invalid_product_ids(example_range) == expected


def test_sum_invalid_product_ids(example_invalid_product_ids):
    assert sum_invalid_product_ids(example_invalid_product_ids) == 1227775554
