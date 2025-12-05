import io
import textwrap

import pytest

from aoc_2025.day_05 import ProductInventory, ProductSatus, solve, parse_id_range, read_inventory_db, product_status


@pytest.fixture
def example_input():
    yield io.StringIO(textwrap.dedent("""\
    3-5
    10-14
    16-20
    12-18
    
    1
    5
    8
    11
    17
    32
    """))

@pytest.fixture
def example_inventory(example_input):
    yield read_inventory_db(example_input)


def test_day05_example(example_input):
    s1, = solve(example_input)
    assert s1 == 3


def test_id_range():
    r = parse_id_range('3-5')
    assert list(r) == [3, 4, 5]


def test_read_inventory_db(example_input):
    id_ranges, product_ids = read_inventory_db(example_input)

    assert id_ranges == {
        parse_id_range('3-5'),
        parse_id_range('10-14'),
        parse_id_range('16-20'),
        parse_id_range('12-18'),
    }
    assert product_ids == {
        1,
        5,
        8,
        11,
        17,
        32
    }


@pytest.mark.parametrize(
    "product_id, expected_status",
    [
        (1, 'spoiled'),
        (5, 'fresh'),
        (8, 'spoiled'),
        (11, 'fresh'),
        (17, 'fresh'),
        (32, 'spoiled'),
    ]
)
def test_product_status(example_inventory: ProductInventory, product_id: int, expected_status: ProductSatus):
    id_ranges, _ = example_inventory
    assert product_status(id_ranges, product_id) == expected_status
