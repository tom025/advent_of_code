import collections
import typing

type Point = tuple[int, int]


def parse_diagram(textio: typing.TextIO) -> tuple[Point, set[Point], int, int]:
    first_line = next(textio).strip()
    source = next((x, 0) for x, c in enumerate(first_line) if c == 'S')
    width = len(first_line)
    spliters = set()
    line_count = 1
    for y, line in enumerate(textio):
        line_count += 1
        for x, c in enumerate(line):
            if c == '^':
                spliters.add((x, y + 1))
                
    return source, spliters, width, line_count


def new_beams(current_beams, splitters) -> tuple[set[int], set[int]]:
    nbs = set()
    hits = set()
    for beam in current_beams:
        if beam in splitters:
            hits.add(beam)
            nbs.add(beam - 1)
            nbs.add(beam + 1)
            continue
        nbs.add(beam)
    return nbs, hits


def splitters_on_row(splitters: collections.abc.Iterable[Point], i: int) -> set[int]:
    return set(x for x, y in splitters if y == i)

def solve(textio: typing.TextIO) -> tuple[int, int]:
    source, splitters, width, height = parse_diagram(textio)
    current_beams = {source[0]}
    splitter_hits = set()
    for r in range(height):
        s = splitters_on_row(splitters, r)
        nbs, hits = new_beams(current_beams, s)
        current_beams = nbs
        splitter_hits.update(set((h, r) for h in hits))

    return sum(1 for _ in splitter_hits), 0

if __name__ == '__main__':
    with open('input.txt') as f:
        s1, _ = solve(f)
    
    print(f"s1: {s1!r}")