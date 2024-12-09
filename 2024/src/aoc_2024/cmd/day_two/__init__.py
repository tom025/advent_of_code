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


def parse_report_line(line: str) -> list[int]:
    return [int(element) for element in line.split(" ")]


def parse_reports(lines: typing.Iterator[str]):
    for line in lines:
        yield parse_report_line(line)


def analyze_reports_file(path: pathlib.Path | str) -> ReportsSummary:
    safe_count = sum(
        1 for report in parse_reports(read_file_lines(path)) if is_safe(report)
    )

    return ReportsSummary(safe_count=safe_count)


def is_safe(report: typing.Iterable[int]) -> bool:
    diffs = [current - next_ for current, next_ in itertools.pairwise(report)]
    first_sign = sign(diffs[0])

    if first_sign == "zero":
        return False

    for diff in diffs:
        if abs(diff) > 3 or sign(diff) != first_sign:
            return False
    return True


if __name__ == "__main__":
    summary = analyze_reports_file("reports.txt")
    print(repr(summary))
