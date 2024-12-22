import textwrap

from aoc_2024.cmd.day_four import (
    vectors,
    match_word,
    count_matches,
    word_search,
    x_match,
    x_word_search,
    submatrices,
)


def test_get_rows():
    board = ("abc", "def", "ghi")

    assert vectors(board, lambda x, y: y) == [
        ["a", "b", "c"],
        ["d", "e", "f"],
        ["g", "h", "i"],
    ]


def test_get_cols():
    board = ("abc", "def", "ghi")

    assert vectors(board, lambda x, y: x) == [
        ["a", "d", "g"],
        ["b", "e", "h"],
        ["c", "f", "i"],
    ]


def test_get_bottom_left_to_top_right_diagonals():
    board = ("abc", "def", "ghi")

    assert vectors(board, lambda x, y: x + y) == [
        ["a"],
        ["b", "d"],
        ["c", "e", "g"],
        ["f", "h"],
        ["i"],
    ]


def test_get_top_left_to_bottom_right_diagonals():
    board = ("abc", "def", "ghi")

    assert vectors(board, lambda x, y: x - y) == [
        ["g"],
        ["d", "h"],
        ["a", "e", "i"],
        ["b", "f"],
        ["c"],
    ]


def test_match_word():
    assert match_word("XMAS", ["X", "M", "A", "S"])
    assert not match_word("XMAS", ["X", "M", "A", "A"])
    assert match_word("XMAS", ["S", "A", "M", "X"])


def test_count_matches():
    assert count_matches("XMAS", "MMMSXXMASM") == 1
    assert count_matches("XMAS", list("MMMSXXMASM")) == 1
    assert count_matches("XMAS", "XMASAMXAMM") == 2


def test_word_search():
    text = textwrap.dedent("""\
    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX
    """)

    word = "XMAS"

    matrix = [list(l) for l in text.splitlines()]

    assert word_search(word, matrix) == 18


def test_sub_matrices():
    text = textwrap.dedent("""\
   .M.S
   ..A.
   .M.S
   ..A.
   """)

    matrix = [list(l) for l in text.splitlines()]

    assert submatrices(matrix, 3)[0:8] == [
        [[".", "M"], [".", "."]],
        [
            [".", "M", "."],
            [".", ".", "A"],
        ],
        [
            ["M", ".", "S"],
            [".", "A", "."],
        ],
        [
            [".", "S"],
            ["A", "."],
        ],
        [
            [".", "M"],
            [".", "."],
            [".", "M"],
        ],
        [[".", "M", "."], [".", ".", "A"], [".", "M", "."]],
        [["M", ".", "S"], [".", "A", "."], ["M", ".", "S"]],
        [[".", "S"], ["A", "."], [".", "S"]],
    ]


def test_x_match():
    assert (
        x_match(
            [
                ["M", ".", "S"],
                [".", "A", "."],
                ["M", ".", "S"],
            ],
            "MAS",
        )
        == True
    )
    assert x_match([[".", "M"], [".", "."], [".", "M"]], "MAS") == False


def test_x_word_search():
    text = textwrap.dedent("""\
    .M.S......
    ..A..MSMS.
    .M.S.MAA..
    ..A.ASMSM.
    .M.S.M....
    ..........
    S.S.S.S.S.
    .A.A.A.A..
    M.M.M.M.M.
    ..........
    """)

    matrix = [list(l) for l in text.splitlines()]

    assert x_word_search(matrix, "MAS") == 9
