import collections
import io
import textwrap
import typing

import pytest

from aoc_2025.day_01 import Rotation, parse_rotation, move_dial, apply_rotations, count_dial_at_zero, parse_rotations, \
    solve


@pytest.fixture
def example_input() -> collections.abc.Generator[typing.TextIO, None, None]:
    yield io.StringIO(textwrap.dedent("""\
        L68
        L30
        R48
        L5
        R60
        L55
        L1
        L99
        R14
        L82
    """))

@pytest.fixture
def example_rotations():
    yield [
        ('L', 68),
        ('L', 30),
        ('R', 48),
        ('L', 5),
        ('R', 60),
        ('L', 55),
        ('L', 1),
        ('L', 99),
        ('R', 14),
        ('L', 82)
    ]

def test_day01_example(example_input: typing.TextIO) -> None:
    assert solve(example_input) == 3

def test_parse_input(example_input: typing.TextIO, example_rotations) -> None:
    assert list(parse_rotations(example_input)) == example_rotations

@pytest.mark.parametrize(
    "rotation_str,expected",
    [
        ('L68', ('L', 68)),
        ('R60', ('R', 60)),
        ('R0', ('R', 0)),
        ('L0', ('L', 0))
    ],
)
def test_parse_rotation(rotation_str, expected):
    assert parse_rotation(rotation_str) == expected

@pytest.mark.parametrize(
    "current_position,rotation,expected",
    [
        (50, ('L', 68), 82),
        (82, ('L', 30), 52),
        (52, ('R', 48), 0)
    ]
)
def test_move_dial(current_position: int, rotation: Rotation, expected: int):
    new_pos, _ = move_dial(current_position, rotation)
    assert new_pos == expected


def test_apply_rotations(example_rotations: list[Rotation]):
    dial_positions: list[int] = list(p for p, _ in apply_rotations(50, iter(example_rotations)))
    assert dial_positions == [
        82,
        52,
        0,
        95,
        55,
        0,
        99,
        0,
        14,
        32
    ]


def test_count_dial_at_zero(example_rotations: list[Rotation]) -> None:
    assert count_dial_at_zero(apply_rotations(50, iter(example_rotations))) == 3

