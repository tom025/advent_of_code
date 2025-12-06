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


def solve(textio: typing.TextIO) -> tuple[int, int]:
    matrix = parse_matrix(textio)
    width = len(matrix[0])
    s1_ = sum(solve_problem(get_problem(matrix, p)) for p in range(width))
    return s1_, 0

if __name__ == '__main__':
    with open('input.txt') as f:
        s1, _ = solve(f)

    print(f"s1: {s1!r}")
