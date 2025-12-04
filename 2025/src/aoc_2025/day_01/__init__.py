from collections import abc
import typing

Direction = typing.Literal['L', 'R']
Rotation = tuple[Direction, int]


def parse_rotation(r: str) -> Rotation:
    return typing.cast(Direction, r[0]), int(r[1:])


def move_dial(pos: int, rotation: Rotation) -> tuple[int]:
    direction, clicks = rotation
    return ((pos + clicks if direction == 'R' else pos - clicks) % 100,)


def apply_rotations(start: int, rotations: abc.Iterator[Rotation]) -> abc.Generator[tuple[int], None, None]:
    pos = start
    for r in rotations:
        pos, = move_dial(pos, r)
        yield pos,


def count_dial_at_zero(dial_positions: abc.Iterator[tuple[int]]) -> int:
    return sum(1 for p, in dial_positions if p == 0)


def parse_rotations(text: typing.TextIO) -> abc.Generator[Rotation, None, None]:
    for line in text:
        yield parse_rotation(line.strip())


def solve(text: typing.TextIO) -> int:
    return count_dial_at_zero(apply_rotations(50, parse_rotations(text)))

if __name__ == '__main__':
    with open('input.txt') as f:
        result = solve(f)

    print(f"password is: {result!r}")