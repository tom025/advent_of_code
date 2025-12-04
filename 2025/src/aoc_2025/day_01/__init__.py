import collections
import itertools
from collections import abc
import typing

Direction = typing.Literal['L', 'R']
Rotation = tuple[Direction, int]


def parse_rotation(r: str) -> Rotation:
    return typing.cast(Direction, r[0]), int(r[1:])


def move_dial(pos: int, rotation: Rotation) -> tuple[int, int]:
    direction, clicks = rotation
    a = pos + clicks if direction == 'R' else pos - clicks
    q, r = divmod(a, 100)
    if direction == 'R' and r == 0:
        q -= 1
    if direction == 'L' and pos == 0:
        q = max(0, abs(q) - 1)
    return r, abs(q)



def apply_rotations(start: int, rotations: abc.Iterator[Rotation]) -> abc.Generator[tuple[int, int], None, None]:
    pos = start
    for r in rotations:
        pos, q = move_dial(pos, r)
        yield pos, q


def calculate_passwords(dial_positions: abc.Iterator[tuple[int, int]]) -> tuple[int, int]:
    def op(acc: tuple[int, int], d: tuple[int, int]):
        zero_positions, zero_passes = acc
        rotation_position, rotation_zero_passes = d

        if rotation_position == 0:
            zero_positions += 1

        zero_passes += rotation_zero_passes

        return zero_positions, zero_passes

    z_pos, z_pass = collections.deque(itertools.accumulate(dial_positions, op, initial=(0, 0)), maxlen=1).pop()
    return z_pos, z_pos + z_pass


def parse_rotations(text: typing.TextIO) -> abc.Generator[Rotation, None, None]:
    for line in text:
        yield parse_rotation(line.strip())


def solve(text: typing.TextIO) -> tuple[int, int]:
    return calculate_passwords(apply_rotations(50, parse_rotations(text)))

if __name__ == '__main__':
    with open('input.txt') as f:
        password, new_security_protocol_password = solve(f)

    print(f"password is: {password!r}")
    print(f"new security protocol password is: {new_security_protocol_password!r}")
