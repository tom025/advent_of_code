from aoc_2024.cmd.day_three import (
    scan_for_instructions,
    sum_instructions,
    enabled_sections,
    sum_instructions_with_directives,
)


def test_scan_for_mul():
    corrupted_instructions = (
        "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    )
    assert tuple(scan_for_instructions(corrupted_instructions)) == (
        ("mul", 2, 4),
        ("mul", 5, 5),
        ("mul", 11, 8),
        ("mul", 8, 5),
    )


def test_extract_enabled_sections():
    corrupted_instructions = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    assert tuple(enabled_sections(corrupted_instructions)) == (
        "xmul(2,4)&mul[3,7]!^",
        "?mul(8,5))",
    )


def test_sum_instructions_with_directives():
    corrupted_instructions = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    assert sum_instructions_with_directives(corrupted_instructions) == 48


def test_sum_instructions():
    instructions = (
        ("mul", 2, 4),
        ("mul", 5, 5),
        ("mul", 11, 8),
        ("mul", 8, 5),
    )

    assert sum_instructions(instructions) == 161
