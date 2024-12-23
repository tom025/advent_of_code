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


def sums(
    page_order_rules: dict[int, frozenset[int]], updates: list[list[int]]
) -> dict[str, int]:
    correctly_ordered, incorrectly_ordered = categorize_updates(
        page_order_rules, updates
    )
    return {
        "sum_of_correctly_ordered_update_middle_pages": sum(
            middle_page(update) for update in correctly_ordered
        ),
        "sum_of_fixed_update_middle_pages": sum(
            middle_page(fix_update(page_order_rules, update))
            for update in incorrectly_ordered
        ),
    }


def categorize_updates(
    page_order_rules: dict[int, frozenset[int]], updates: list[list[int]]
) -> tuple[list[list[int]], list[list[int]]]:
    correctly_ordered = []
    not_correctly_ordered = []
    for update in updates:
        if is_correctly_ordered(page_order_rules, update):
            correctly_ordered.append(update)
        else:
            not_correctly_ordered.append(update)
    return correctly_ordered, not_correctly_ordered


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


def fix_update(
    page_order_rules: dict[int, frozenset[int]], update: list[int]
) -> list[int]:
    broken_rules = find_broken_rules(page_order_rules, update)

    while len(broken_rules) > 0:
        page, after_page = next(iter(broken_rules))
        a, b = update.index(page), update.index(after_page)
        update[b], update[a] = update[a], update[b]
        broken_rules = find_broken_rules(page_order_rules, update)

    return update


def find_broken_rules(page_order_rules, update):
    broken_rules = set()
    for idx, page in enumerate(update):
        pages_before = frozenset(update[0:idx])
        intersection = page_order_rules[page].intersection(pages_before)
        if len(intersection) != 0:
            for e in intersection:
                broken_rules.add((page, e))
    return broken_rules


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        sums_ = sums(*safety_manual_updates(file))

    print(sums_)
