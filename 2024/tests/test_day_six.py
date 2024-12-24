import textwrap
import typing

import pytest

from aoc_2024.cmd.day_six import Map


def test_load_map_from_text():
    map_text = textwrap.dedent("""\
      ....#.....
      .........#
      ..........
      ..#.......
      .......#..
      ..........
      .#..^.....
      ........#.
      #.........
      ......#...
    """)

    map_ = Map.from_(map_text)
    assert map_ == Map(
        dim=(10, 10),
        guard_loc=(4, 6),
        guard_direction="up",
        guard_location_history=[(4, 6)],
        obstruction_locs=frozenset(
            {(4, 0), (9, 1), (2, 3), (7, 4), (1, 6), (8, 7), (0, 8), (6, 9)}
        ),
    )


def test_next_map():
    map_text = textwrap.dedent("""\
      ....#.....
      .........#
      ..........
      ..#.......
      .......#..
      ..........
      .#..^.....
      ........#.
      #.........
      ......#...
    """)

    map_ = Map.from_(map_text)

    next_map = next(map_)
    assert next_map == Map(
        dim=(10, 10),
        guard_loc=(4, 7),
        guard_direction="up",
        guard_location_history=[(4, 6), (4, 7)],
        obstruction_locs=frozenset(
            {(4, 0), (9, 1), (2, 3), (7, 4), (1, 6), (8, 7), (0, 8), (6, 9)}
        ),
    )


def test_next_map_when_obstructed():
    map_text = textwrap.dedent("""\
      ....#.....
      ....^....#
      ..........
      ..#.......
      .......#..
      ..........
      .#........
      ........#.
      #.........
      ......#...
    """)

    map_ = Map.from_(map_text)

    assert next(map_) == Map(
        dim=(10, 10),
        guard_loc=(5, 1),
        guard_direction="right",
        guard_location_history=[(4, 1), (5, 1)],
        obstruction_locs=frozenset(
            {(4, 0), (9, 1), (2, 3), (7, 4), (1, 6), (8, 7), (0, 8), (6, 9)}
        ),
    )


def test_stops_iteration_when_next_is_out_of_bounds():
    map_text = textwrap.dedent("""\
      ....#.....
      .........#
      ..........
      ..#.......
      .......#..
      ..........
      .#........
      ........#.
      #.........
      ......#v..
    """)

    map_ = Map.from_(map_text)

    with pytest.raises(StopIteration):
        next(map_)


def test_count_distinct_guard_positions():
    map_text = textwrap.dedent("""\
      ....#.....
      .........#
      ..........
      ..#.......
      .......#..
      ..........
      .#..^.....
      ........#.
      #.........
      ......#...
    """)

    map_ = Map.from_(map_text)

    *_, last = iter(map_)

    assert len(frozenset(last.guard_location_history)) == 41
