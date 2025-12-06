import io
import operator
import textwrap

import pytest

from aoc_2025.day_06 import solve, parse_matrix, get_problem, solve_problem, Problem


@pytest.fixture
def example_input():
    yield io.StringIO(textwrap.dedent("""\
    123 328  51 64 
     45 64  387 23 
      6 98  215 314
    *   +   *   +  
    """))

@pytest.fixture
def example_matrix():
    yield [
        [123, 328, 51, 64],
        [45, 64, 387, 23],
        [6, 98, 215, 314],
        [operator.mul, operator.add, operator.mul, operator.add]
    ]


def test_day06_example(example_input) -> None:
    s1, _ = solve(example_input)
    assert s1 == 4277556


def test_parse_matrix(example_input, example_matrix):
    assert parse_matrix(example_input) == example_matrix


@pytest.mark.parametrize(
    "col_index, expected",
    [
        (0, (operator.mul, 123, 45, 6)),
        (1, (operator.add, 328, 64, 98)),
        (2, (operator.mul, 51, 387, 215)),
        (3, (operator.add, 64, 23, 314)),
    ]
)
def test_get_problem(example_matrix, col_index, expected):
    assert get_problem(example_matrix, col_index) == expected


@pytest.mark.parametrize(
    "col_index, expected",
    [
        (0, 33210),
        (1, 490),
        (2, 4243455),
        (3, 401)
    ]
)
def test_solve_problem(example_matrix, col_index, expected):
    assert solve_problem(get_problem(example_matrix, col_index)) == expected

