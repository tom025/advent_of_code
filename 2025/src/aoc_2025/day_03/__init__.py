import collections
import typing


def to_joltages(bank: str) -> list[int]:
    return list(int(i) for i in bank)


def parse_banks(textio: typing.TextIO) -> collections.abc.Generator[list[int], None, None]:
    for line in textio:
        yield to_joltages(line.strip())


def max_joltage(bank: list[int]) -> int:
    return max(
        int(str(j) + str(max(bank[i + 1:])))
        for i, j in enumerate(bank)
        if i < len(bank) - 1
    )


def max_joltages(banks: collections.abc.Iterator[list[int]]) -> collections.abc.Generator[int, None, None]:
    for bank in banks:
        yield max_joltage(bank)


def solve(textio: typing.TextIO) -> int:
    return sum(max_joltages(parse_banks(textio)))

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        solution = solve(f)

    print(f'sum of max joltages: {solution!r}')