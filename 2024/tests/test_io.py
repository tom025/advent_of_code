import io
import pathlib
import textwrap

from aoc_2024 import io as aoc_io


def test_generate_lines():
    list_text = """\
    1234   4567
    8901   2345
    6789   1234
    """

    content = io.StringIO(textwrap.dedent(list_text))

    assert tuple(line for line in aoc_io.to_lines(content)) == (
        "1234   4567",
        "8901   2345",
        "6789   1234",
    )


def test_read_file_lines(tmp_path: pathlib.Path):
    list_text = """\
    1234   4567
    8901   2345
    6789   1234
    """
    path = tmp_path.joinpath("lines")
    with open(path, "w") as file:
        file.write(textwrap.dedent(list_text))

    assert tuple(aoc_io.read_file_lines(path)) == (
        "1234   4567",
        "8901   2345",
        "6789   1234",
    )
