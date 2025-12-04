import collections
import typing


def solve(input: typing.TextIO) -> int:
    raise NotImplementedError()


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


def find_invalid_product_ids(r: range) -> list[int]:
    return list(
        product_id
        for product_id in r
        if not is_valid_product_id(product_id)
    )
