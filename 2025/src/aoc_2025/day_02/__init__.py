import collections
import itertools
import typing



def parse_range(id_range_text: str):
    start_str, end_str = id_range_text.split('-')
    return range(int(start_str), int(end_str) + 1)


def parse_ranges(input: typing.TextIO) -> collections.abc.Generator[range, None, None]:
    for id_range_text in input.read().split(','):
        yield parse_range(id_range_text)


def is_valid_product_id(id: int) -> bool:
    id_str = str(id)
    mid, r = divmod(len(id_str), 2)
    if r != 0:
        return True
    first = id_str[:mid]
    second = id_str[mid:]
    if first != second:
        return True
    return False

def is_valid_product_id_new_rules(id: int) -> bool:
    return True


def find_invalid_product_ids(r: range) -> list[int]:
    return list(
        product_id
        for product_id in r
        if not is_valid_product_id(product_id)
    )

def find_invalid_product_ids_new_rules(r: range) -> list[int]:
    return list(
        product_id
        for product_id in r
        if not is_valid_product_id_new_rules(product_id)
    )


def invalid_product_ids_for_ranges(ranges: collections.abc.Iterable[range]) -> collections.abc.Generator[tuple[list[int], list[int]], None, None]:
    for r in ranges:
        yield find_invalid_product_ids(r), find_invalid_product_ids_new_rules(r)


def sum_invalid_product_ids(range_invalid_ids: collections.abc.Iterator[tuple[list[int], list[int]]]) -> tuple[int, int]:
    def op(acc: tuple[int, int], sums: tuple[int, int]) -> tuple[int, int]:
        sum_invalid_ids, sum_invalid_ids_new_rules = acc
        s1, s2 = sums
        return sum_invalid_ids + s1, sum_invalid_ids_new_rules + s2

    return collections.deque(
        itertools.accumulate(
            ((sum(invalid_ids), sum(invalid_ids_new_rules)) for invalid_ids, invalid_ids_new_rules in range_invalid_ids),
            op,
            initial=(0, 0)
        )
    ).pop()

def solve(textio: typing.TextIO) -> tuple[int, int]:
    return sum_invalid_product_ids(invalid_product_ids_for_ranges(parse_ranges(textio)))


if __name__ == '__main__':
    with open('input.txt') as f:
        s1, s2 = solve(f)

    print(f"sum of all invalid product ids across ranges: {s1!r}")
    print(f"sum of all invalid product ids across ranges with new rules: {s2!r}")
