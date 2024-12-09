import os
import typing
from typing import Generator


def to_lines(content: typing.TextIO) -> Generator[str, None, None]:
    for line in content:
        yield line.rstrip()


def read_file_lines(path: os.PathLike | str) -> Generator[str, None, None]:
    with open(path, "r") as f:
        yield from to_lines(f)
