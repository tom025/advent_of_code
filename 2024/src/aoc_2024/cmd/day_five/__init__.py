import collections
import itertools
import typing


def parse_input(
    input_: typing.TextIO,
) -> typing.Generator[typing.Sequence[str | int], None, None]:
    past_break = False
    for line in input_:
        l = line.rstrip()
        if l == "":
            past_break = True
            continue

        if not past_break:
            yield "page_order_rule", tuple(int(c) for c in l.split("|"))

        if past_break:
            yield "update", [int(c) for c in l.split(",")]


def safety_manual_updates(
    input_: typing.TextIO,
) -> tuple[dict[int, frozenset[int]], list[list[int]]]:
    elements = [element for element in parse_input(input_)]
    rules = [rule for type_, rule in elements if type_ == "page_order_rule"]
    kf = lambda rule: rule[0]
    rules_by_page = collections.defaultdict(
        frozenset,
        {
            page: frozenset(rule[1] for rule in rules)
            for page, rules in itertools.groupby(sorted(rules, key=kf), kf)
        },
    )
    updates = [update for type_, update in elements if type_ == "update"]
    return rules_by_page, updates


def sum_of_correctly_ordered_update_middle_pages(
    page_order_rules: dict[int, frozenset[int]], updates: list[list[int]]
) -> int:
    return sum(
        middle_page(update)
        for update in updates
        if is_correctly_ordered(page_order_rules, update)
    )


def is_correctly_ordered(
    page_order_rules: dict[int, frozenset[int]], update: list[int]
) -> bool:
    for idx, page in enumerate(update):
        pages_before = frozenset(update[0:idx])
        if len(page_order_rules[page].intersection(pages_before)) != 0:
            return False
    return True


def middle_page(update: list[int]) -> int:
    return update[len(update) // 2]


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        sum_ = sum_of_correctly_ordered_update_middle_pages(
            *safety_manual_updates(file)
        )

    print(f"sum of correctly ordered update middle pages: {sum_}")
