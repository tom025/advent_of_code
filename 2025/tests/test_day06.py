import io
import operator
import textwrap

import pytest

from aoc_2025.day_06 import solve, parse_matrix, get_problem, solve_problem, parse_caphalopod_problems, \
    solve_caphalopod_problem


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
    s1, s2 = solve(example_input)
    assert s1 == 4277556
    assert s2 == 3263827


def test_parse_matrix(example_input, example_matrix):
    assert parse_matrix(example_input) == example_matrix


@pytest.mark.parametrize(
    "problem_index, expected_problem",
    [
        (
                0,
                (
                        operator.mul,
                        [
                            [1, 2, 3],
                            [0, 4, 5],
                            [0, 0, 6]
                        ]
                )
        ),
        (
                1,
                (
                        operator.add,
                        [
                            [3, 2, 8],
                            [6, 4, 0],
                            [9, 8, 0]
                        ]
                )
        ),
        (
                2,
                (
                        operator.mul,
                        [
                            [0, 5, 1],
                            [3, 8, 7],
                            [2, 1, 5]
                        ]
                )
        ),
        (
                3,
                (
                        operator.add,
                        [
                            [6, 4, 0],
                            [2, 3, 0],
                            [3, 1, 4]
                        ]
                )
        )
    ]
)
def test_parse_caphalopod_problems(example_input, problem_index, expected_problem):
    assert parse_caphalopod_problems(example_input)[problem_index] == expected_problem


@pytest.mark.parametrize(
    "problem, expected_solution",
    [
        (
                (
                        operator.mul,
                        [
                            [1, 2, 3],
                            [0, 4, 5],
                            [0, 0, 6]
                        ]
                ),
                8544
        ),
        (
                (
                        operator.add,
                        [
                            [3, 2, 8],
                            [6, 4, 0],
                            [9, 8, 0]
                        ]
                ),
                625
        ),
        (
                (
                        operator.mul,
                        [
                            [0, 5, 1],
                            [3, 8, 7],
                            [2, 1, 5]
                        ]
                ),
                3253600
        ),
        (
                (
                        operator.add,
                        [
                            [6, 4, 0],
                            [2, 3, 0],
                            [3, 1, 4]
                        ]
                ),
                1058
        )
    ]
)
def test_solve_caphalopod_problem(problem, expected_solution):
    assert solve_caphalopod_problem(problem) == expected_solution

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
