import io
import textwrap

from src.aoc_2024_one import (
    to_lines,
    parse_line,
    to_left_right,
    sort_lists,
    calculate_total_distance_from,
)


def test_parse_lines():
    list_text = """\
    1234   4567
    8901   2345
    6789   1234
    """

    content = io.StringIO(textwrap.dedent(list_text))

    assert tuple(l for l in to_lines(content)) == (
        "1234   4567",
        "8901   2345",
        "6789   1234",
    )


def test_split_lists():
    lines = (
        "1234   4567",
        "8901   2345",
        "6789   1234",
    )

    assert tuple(parse_line(l) for l in lines) == (
        (1234, 4567),
        (8901, 2345),
        (6789, 1234),
    )


def test_to_left_right():
    parsed_lines = ((1234, 4567), (8901, 2345), (6789, 1234))

    assert tuple(to_left_right(iter(parsed_lines))) == (
        (1234, 8901, 6789),
        (4567, 2345, 1234),
    )


def test_sort_lists():
    unsorted = ((1234, 8901, 6789), (4567, 2345, 1234))

    assert tuple(sort_lists(iter(unsorted))) == ([1234, 6789, 8901], [1234, 2345, 4567])


def test_calculate_total_distance_from_text():
    list_text = """\
    1234   4567
    8901   2345
    6789   1234
    """

    content = io.StringIO(textwrap.dedent(list_text))
    assert calculate_total_distance_from(content) == 8778
