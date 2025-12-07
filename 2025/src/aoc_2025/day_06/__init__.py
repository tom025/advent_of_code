import itertools
import operator
import typing


Operator = typing.Callable[[int, int], int]
ProblemSymbols = Operator | int
Problem = tuple[Operator, int, ...]


def parse_value(value: str) -> ProblemSymbols:
    match value:
        case '*':
            return operator.mul
        case '+':
            return operator.add
        case _:
            return int(value)


def parse_matrix(textio: typing.TextIO) -> list[list[ProblemSymbols]]:
    return list(
        list(
            parse_value(v)
            for v in line.strip().split(' ')
            if v != ''
        )
        for line in textio
    )


def get_problem(matrix: list[list[ProblemSymbols]] , i: int) -> Problem:
    m_height = len(matrix)
    symbols = list(matrix[y][i] for y in range(m_height))
    return typing.cast(Problem, tuple(symbols[m_height-1:m_height] + symbols[:m_height-1]))


def solve_problem(p: Problem) -> int:
    op, *ints = p
    *_, result = itertools.accumulate(ints, op)
    return result


def int_or_zero(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        return 0


def find_ops_and_prob_ranges(operations_line: str) -> list[tuple[Operator, int, int]]:
    result = []
    p_start = 0
    op = None
    for i in range(len(operations_line)):
        if i == len(operations_line) - 1:
            result.append((op, p_start, i))
        c = operations_line[i]
        if c in {'+', '*'}:
            if i > 0:
                result.append((op, p_start, i - 1))
            op = parse_value(c)
            p_start = i
    return result


def parse_caphalopod_problems(textio: typing.TextIO) -> list[tuple[Operator, list[list[int]]]]:
    lines = textio.readlines()
    num_lines = lines[:len(lines) - 1]
    operations = lines[-1]

    op_and_prob_ranges = find_ops_and_prob_ranges(operations)
    return list(
        (
            op,
            list(list(int_or_zero(c) for c in l[start:stop]) for l in num_lines)
        )
        for op, start, stop in op_and_prob_ranges
    )


def matrix_col(matrix: list[list[int]], i: int) -> list[int]:
    return list(matrix[y][i] for y in range(len(matrix)) if matrix[y][i] != 0)


def digits_to_number(digits: list[int]) -> int:
    return sum(
        d * (10 ** (len(digits) - i - 1)) for i, d in enumerate(digits)
    )


def solve_caphalopod_problem(problem: tuple[Operator, list[list[int]]]) -> int:
    op, matrix = problem
    m_width = len(matrix[0])

    *_, result = itertools.accumulate(
        (
            digits_to_number(matrix_col(matrix, x))
            for x in reversed(range(m_width))
        ),
        op
    )

    return result

def solve(textio: typing.TextIO) -> tuple[int, int]:
    matrix = parse_matrix(textio)
    width = len(matrix[0])
    s1_ = sum(solve_problem(get_problem(matrix, p)) for p in range(width))

    textio.seek(0)
    s2_ = sum(solve_caphalopod_problem(p) for p in parse_caphalopod_problems(textio))
    return s1_, s2_

if __name__ == '__main__':
    with open('input.txt') as f:
        s1, s2 = solve(f)

    print(f"s1: {s1!r}")
    print(f"s2: {s2!r}")
