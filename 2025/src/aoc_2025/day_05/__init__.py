import typing

ProductInventory = tuple[set[range], set[int]]
ProductSatus = typing.Literal['fresh', 'spoiled']


def read_inventory_db(textio: typing.TextIO) -> tuple[set[range], set[int]]:
    id_ranges = set()
    for line in textio:
        l = line.strip()
        if l == '':
            break
        id_ranges.add(parse_id_range(l))

    product_ids = set()
    for line in textio:
        l = line.strip()
        product_ids.add(int(l))

    return id_ranges, product_ids


def parse_id_range(s: str):
    start, stop = s.split('-')
    return range(int(start), int(stop) + 1)


def product_status(id_ranges: set[range], product_id: int) -> ProductSatus:
    if any(True for r in id_ranges if product_id in r):
        return 'fresh'
    return 'spoiled'


def solve(textio: typing.TextIO) -> tuple[int]:
    id_ranges, product_ids = read_inventory_db(textio)
    s1_ = sum(1 for pid in product_ids if product_status(id_ranges, pid) == 'fresh')
    return s1_,

if __name__ == '__main__':
    with open('input.txt') as f:
        s1, = solve(f)

    print(f"fresh product count: {s1!r}")
