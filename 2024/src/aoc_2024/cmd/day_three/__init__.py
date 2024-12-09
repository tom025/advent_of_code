import os
import re
import typing
from dataclasses import dataclass
from typing import Iterator

type InstructionName = typing.Literal["mul"]
type Instruction = tuple[InstructionName, int, ...]


@dataclass
class InstructionsSummary:
    sum_of_mul: int
    sum_of_mul_with_directives: int


def sum_instructions_file(path: os.PathLike | str) -> InstructionsSummary:
    with open(path, "r") as file:
        corrupted_instructions = file.read()
    return InstructionsSummary(
        sum_of_mul=sum_instructions(scan_for_instructions(corrupted_instructions)),
        sum_of_mul_with_directives=sum_instructions_with_directives(
            corrupted_instructions
        ),
    )


def scan_for_instructions(currupted_instructions: str) -> typing.Iterator:
    for match in re.finditer(
        re.compile(r"(?P<instruction>mul)\((?P<args>\d+,\d+)\)"), currupted_instructions
    ):
        yield (
            match.group("instruction"),
            *tuple(int(arg) for arg in match.group("args").split(",")),
        )


def sum_instructions(instructions: Iterator[Instruction]) -> int:
    return sum(arg_1 * arg_2 for _, arg_1, arg_2 in instructions)


enable_directive = "do()"
disable_directive = "don't()"


def toggle_directive(directive):
    if directive == enable_directive:
        return disable_directive
    return enable_directive


def enabled_sections(corrupted_instructions: str):
    directive = disable_directive
    while len(corrupted_instructions) > 0:
        found = corrupted_instructions.find(directive)
        boundary = found if found != -1 else len(corrupted_instructions)

        if directive == disable_directive:
            yield corrupted_instructions[:boundary]
        corrupted_instructions = corrupted_instructions[
            boundary + len(directive) : len(corrupted_instructions)
        ]
        directive = toggle_directive(directive)


def sum_instructions_with_directives(corrupted_instructions: str) -> int:
    return sum(
        sum_instructions(scan_for_instructions(section))
        for section in enabled_sections(corrupted_instructions)
    )


if __name__ == "__main__":
    print(repr(sum_instructions_file("corrupted_instructions.txt")))
