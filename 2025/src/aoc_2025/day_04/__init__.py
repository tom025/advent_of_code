import typing

symbols = typing.Literal['.', '@']


def to_matrix(textio: typing.TextIO) -> list[list[symbols]]:
    return typing.cast(list[list[symbols]], list(list(line.strip()) for line in textio))


def neighbours(matrix: list[list[typing.Any]], point: tuple[int, int]) -> list[list[typing.Any]]:
    m_width, m_height = len(matrix[0]), len(matrix)
    x, y = point
    col_before = x - 1
    row_before = y - 1
    col_after = x + 1
    row_after = y + 1

    result = []
    if row_before >= 0:
        result.append(matrix[row_before][max(col_before, 0): min(col_after + 1, m_width)])

    current_row = []
    if col_before >= 0:
        current_row.append(matrix[y][col_before])

    if col_after < m_width:
        current_row.append(matrix[y][col_after])

    result.append(current_row)

    if row_after < m_height:
        result.append(matrix[row_after][max(col_before, 0): min(col_after + 1, m_width)])

    return result


def all_points(matrix: list[list[typing.Any]]) -> typing.Generator[tuple[int, int], None, None]:
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            yield x, y


def solve(textio: typing.TextIO) -> typing.Tuple[int]:
    matrix = to_matrix(textio)

    symbol_counts = (
        count_symbol(neighbours(matrix, (x, y)), '@')
        for x, y in all_points(matrix)
        if matrix[y][x] == '@'
    )
    return sum(1 for sc in symbol_counts if sc < 4),


def count_symbol(ns: list[list[symbols]], symbol: symbols) -> int:
    return sum(
        sum(
            1 for sym in row if sym == symbol
        )
        for row in ns
    )

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        s1, = solve(f)

    print(f"paper rolls with less than 4 paper rolls as neighbours: {s1!r}")