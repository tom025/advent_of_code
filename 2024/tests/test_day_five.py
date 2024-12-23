import collections

import pytest
import io
import textwrap

from aoc_2024.cmd.day_five import (
    safety_manual_updates,
    sums,
    is_correctly_ordered,
    middle_page,
    fix_update,
)


def test_parse_input():
    text = textwrap.dedent("""\
    47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47
    """)

    page_order_rules, updates = safety_manual_updates(io.StringIO(text))

    print(repr(page_order_rules))

    assert len(page_order_rules) == 6
    assert page_order_rules[47] == frozenset({13, 29, 53, 61})
    assert page_order_rules[97] == frozenset({75, 13, 47, 61, 53, 29})
    assert page_order_rules[13] == frozenset()

    assert len(updates) == 6
    assert updates[0] == [75, 47, 61, 53, 29]
    assert updates[2] == [75, 29, 13]

    sums_ = sums(page_order_rules, updates)
    assert sums_["sum_of_correctly_ordered_update_middle_pages"] == 143
    assert sums_["sum_of_fixed_update_middle_pages"] == 123


example_page_order_rules = collections.defaultdict(
    frozenset,
    {
        29: frozenset({13}),
        47: frozenset({29, 13, 61, 53}),
        53: frozenset({13, 29}),
        61: frozenset({29, 53, 13}),
        75: frozenset({13, 47, 29, 53, 61}),
        97: frozenset({75, 13, 47, 61, 53, 29}),
    },
)


@pytest.mark.parametrize(
    ["update", "expected"],
    [
        ([75, 47, 61, 53, 29], True),
        ([97, 61, 53, 29, 13], True),
        ([75, 29, 13], True),
        ([75, 97, 47, 61, 53], False),
        ([61, 13, 29], False),
        ([97, 13, 75, 29, 47], False),
    ],
)
def test_is_correctly_ordered(update, expected):
    assert is_correctly_ordered(example_page_order_rules, update) == expected


@pytest.mark.parametrize(
    ["update", "expected"],
    [
        ([75, 47, 61, 53, 29], 61),
        ([97, 61, 53, 29, 13], 53),
        ([75, 29, 13], 29),
    ],
)
def test_middle_page(update, expected):
    assert middle_page(update) == expected


@pytest.mark.parametrize(
    ["update", "fixed"],
    [
        ([75, 97, 47, 61, 53], [97, 75, 47, 61, 53]),
        ([61, 13, 29], [61, 29, 13]),
        ([97, 13, 75, 29, 47], [97, 75, 47, 29, 13]),
    ],
)
def test_fix_update(update, fixed):
    assert fix_update(example_page_order_rules, update) == fixed
