import textwrap

import pytest

from aoc_2024.cmd.day_six import Map, InfiniteLoopError


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
        guard_location_history=frozenset({((4, 6), "up")}),
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
        guard_loc=(4, 5),
        guard_direction="up",
        guard_location_history=frozenset({((4, 6), "up"), ((4, 7), "up")}),
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
        guard_location_history=frozenset({((4, 1), "up"), ((5, 1), "right")}),
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

    assert last.distinct_guard_positions == 41


@pytest.mark.timeout(1)
def test_error_when_in_loop():
    map_text = textwrap.dedent("""\
      ....#.....
      .........#
      ..........
      ..#.......
      .......#..
      ..........
      .#.#^.....
      ........#.
      #.........
      ......#...
    """)

    map_ = Map.from_(map_text)

    with pytest.raises(InfiniteLoopError):
        *_, last = map_
