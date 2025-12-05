import collections
import typing


def to_joltages(bank: str) -> list[int]:
    return list(int(i) for i in bank)


def parse_banks(textio: typing.TextIO) -> collections.abc.Generator[list[int], None, None]:
    for line in textio:
        yield to_joltages(line.strip())

def max_with_index(ints: list[int]) -> tuple[int, int]:
    if len(ints) == 0:
        raise ValueError('no ints')

    max_index = 0
    max_value = ints[max_index]
    for i, v in enumerate(ints[1:]):
        if v > max_value:
            max_index = i + 1
            max_value = v
    return max_index, max_value

def max_joltage(bank: list[int], batteries_allowed: int = 2) -> int:
    window_start = 0
    result = 0
    for i in range(1, batteries_allowed + 1):
        window_end = len(bank) - (batteries_allowed - i)
        window = bank[window_start:window_end]

        max_index, max_value = max_with_index(window)

        result += max_value * (10 ** (batteries_allowed - i))
        window_start = window_start + max_index + 1

    return result


def max_joltages(banks: collections.abc.Iterator[list[int]]) -> collections.abc.Generator[int, None, None]:
    for bank in banks:
        yield max_joltage(bank)


def solve(textio: typing.TextIO) -> int:
    return sum(max_joltages(parse_banks(textio)))

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        solution = solve(f)

    print(f'sum of max joltages: {solution!r}')