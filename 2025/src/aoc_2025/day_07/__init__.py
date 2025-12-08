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


def new_beams(current_beams: dict[int, int], splitters: set[int]) -> tuple[dict[int, int], set[int]]:
    hits = set()
    nbs = collections.defaultdict(int, current_beams)
    for beam_pos, path_count in current_beams.items():
        if beam_pos in splitters:
            hits.add(beam_pos)
            current = current_beams[beam_pos]
            del nbs[beam_pos]
            nbs[beam_pos - 1] += current
            nbs[beam_pos + 1] += current
            
            continue
    return nbs, hits


def splitters_on_row(splitters: collections.abc.Iterable[Point], i: int) -> set[int]:
    return set(x for x, y in splitters if y == i)

def solve(textio: typing.TextIO) -> tuple[int, int]:
    source, splitters, width, height = parse_diagram(textio)
    current_beams = collections.defaultdict(int, {
        source[0]: 1
    })
    splitter_hits = set()
    for r in range(height):
        s = splitters_on_row(splitters, r)
        current_beams, hits = new_beams(current_beams, s)
        splitter_hits.update(set((h, r) for h in hits))

    return sum(1 for _ in splitter_hits), sum(v for v in current_beams.values())

if __name__ == '__main__':
    with open('input.txt') as f:
        s1, s2 = solve(f)
    
    print(f"s1: {s1!r}")
    print(f"s2: {s2!r}")
