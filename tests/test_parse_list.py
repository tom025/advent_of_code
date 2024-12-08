import io
import textwrap

from aoc_2024_one import (
    to_lines,
    parse_line,
    to_left_right,
    sort_lists,
    total_distance,
)
from src.aoc_2024_one import extract_location_lists, similarity_score


def test_generate_lines():
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


def test_parse_lines():
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


def test_extract_location_lists():
    list_text = """\
    1234   4567
    8901   2345
    6789   1234
    """
    content = io.StringIO(textwrap.dedent(list_text))
    assert tuple(extract_location_lists(content)) == (
        (1234, 8901, 6789),
        (4567, 2345, 1234),
    )


def test_calculate_total_distance_from_text():
    lists = (
        (1234, 8901, 6789),
        (4567, 2345, 1234),
    )
    assert total_distance(iter(lists)) == 8778


def test_similarity_score():
    lists = (
        (1234, 8901, 6789),
        (4567, 2345, 1234),
    )

    assert similarity_score(iter(lists)) == 1234
