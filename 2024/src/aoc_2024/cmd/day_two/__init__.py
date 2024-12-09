import collections.abc
import itertools
import pathlib
import typing
from dataclasses import dataclass

from aoc_2024.io import read_file_lines

type Sign = typing.Literal["+"] | typing.Literal["-"] | typing.Literal["zero"]


def sign(n: int) -> Sign:
    if n < 0:
        return "-"
    if n > 0:
        return "+"
    return "zero"


@dataclass
class ReportsSummary:
    safe_count: int
    safe_with_dampening_count: int


def parse_report_line(line: str) -> list[int]:
    return [int(element) for element in line.split(" ")]


def parse_reports(lines: typing.Iterator[str]):
    for line in lines:
        yield parse_report_line(line)


def analyze_reports_file(path: pathlib.Path | str) -> ReportsSummary:
    reports = list(parse_reports(read_file_lines(path)))
    return ReportsSummary(
        safe_count=sum(1 for report in reports if is_safe(report)),
        safe_with_dampening_count=sum(
            1 for report in reports if is_safe(report, with_dampening=True)
        ),
    )


def without_idx[T](iter_: collections.abc.Collection, idx: int) -> typing.Collection[T]:
    return iter_[0 : idx - len(iter_)] + iter_[idx + 1 : len(iter_)]


def is_safe(report: typing.Collection[int], with_dampening: bool = False) -> bool:
    diffs = [current - next_ for current, next_ in itertools.pairwise(report)]
    first_sign = sign(diffs[0])
    for idx, diff in enumerate(diffs):
        if abs(diff) > 3 or sign(diff) != first_sign or first_sign == 'zero':
            if not with_dampening:
                return False
            else:
                return any(
                    is_safe(without_idx(report, idx), with_dampening=False) for idx, _ in enumerate(report)
                )
    return True


if __name__ == "__main__":
    summary = analyze_reports_file("reports.txt")
    print(repr(summary))
