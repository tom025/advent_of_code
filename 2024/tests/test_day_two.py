import collections
import pathlib

import pytest
import textwrap

from aoc_2024.cmd.day_two import (
    analyze_reports_file,
    parse_report_line,
    is_safe,
    remove_level,
    ReportsSummary,
)


def test_day_two(tmp_path: pathlib.Path):
    reports = textwrap.dedent("""\
    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9
    """)

    path = tmp_path.joinpath("reports.txt")
    with open(path, "w") as file:
        file.write(reports)

    summary = analyze_reports_file(path)

    assert summary == ReportsSummary(safe_count=2, safe_with_dampening_count=4)


def test_parse_report_line():
    assert parse_report_line("7 6 4 2 1") == [7, 6, 4, 2, 1]


def idfn(val):
    if isinstance(val, collections.abc.Iterable):
        return repr(val)


@pytest.mark.parametrize(
    "report,expected",
    [
        ([7, 6, 4, 2, 1], True),
        ([1, 2, 7, 8, 9], False),
        ([9, 7, 6, 2, 1], False),
        ([1, 3, 2, 4, 5], False),
        ([8, 6, 4, 4, 1], False),
        ([1, 3, 6, 7, 9], True),
    ],
    ids=idfn,
)
def test_is_safe_report(report: list[int], expected: bool):
    assert is_safe(report) == expected


@pytest.mark.parametrize(
    "report,expected",
    [
        ([7, 6, 4, 2, 1], True),
        ([1, 2, 7, 8, 9], False),
        ([9, 7, 6, 2, 1], False),
        ([1, 3, 2, 4, 5], True),
        ([8, 6, 4, 4, 1], True),
        ([1, 3, 6, 7, 9], True),
    ],
    ids=idfn,
)
def test_is_safe_report_with_dampening(report: list[int], expected: bool):
    assert is_safe(report, with_dampening=True) == expected


def test_without_idx():
    list_ = [0, 1, 2, 3, 4]
    assert [remove_level(list_, idx) for idx, _ in enumerate(list_)] == [
        [1, 2, 3, 4],
        [0, 2, 3, 4],
        [0, 1, 3, 4],
        [0, 1, 2, 4],
        [0, 1, 2, 3],
    ]
