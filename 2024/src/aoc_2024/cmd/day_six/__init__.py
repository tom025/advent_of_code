import dataclasses
import typing

type Coord = tuple[int, int]
type Direction = typing.Literal["left", "up", "right", "down"]


def text_to_matrix(text: str) -> list[list[str]]:
    return [list(line) for line in text.splitlines()]


def coords(matrix: list[list[str]]) -> typing.Generator[tuple[int, int], None, None]:
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            yield x, y


guard_symbols = {"^": "up", ">": "right", "<": "left", "v": "down"}


class Matrix:
    @classmethod
    def from_text(cls, text: str):
        return cls([list(line) for line in text.splitlines()])

    def __init__(self, m: list[list[str]]):
        self.__m = m

    def __iter__(self) -> typing.Generator[tuple[int, int, str], None, None]:
        x_dim, y_dim = self.dim
        for y in range(y_dim):
            for x in range(x_dim):
                yield x, y, self.__m[y][x]

    @property
    def dim(self):
        return len(self.__m[0]), len(self.__m)


def turn_clockwise_90(direction: Direction) -> Direction:
    match direction:
        case "up":
            return "right"
        case "right":
            return "down"
        case "down":
            return "left"
        case "left":
            return "up"


@dataclasses.dataclass
class Map:
    @classmethod
    def from_(cls, text: str):
        guard_loc = None
        guard_direction = None
        obstruction_locs: list[Coord] = []

        matrix = Matrix.from_text(text)
        for x, y, symbol in matrix:
            if symbol in guard_symbols:
                guard_loc = (x, y)
                guard_direction = guard_symbols[symbol]

            if symbol == "#":
                obstruction_locs.append((x, y))

        return cls(
            dim=matrix.dim,
            guard_loc=guard_loc,
            guard_direction=guard_direction,
            guard_location_history=[guard_loc],
            obstruction_locs=frozenset(obstruction_locs),
        )

    dim: Coord
    guard_loc: Coord
    guard_direction: Direction
    guard_location_history: list[Coord]
    obstruction_locs: frozenset[Coord]

    def __init__(
        self,
        dim: Coord,
        guard_loc: Coord,
        guard_direction: Direction,
        guard_location_history: list[Coord],
        obstruction_locs: frozenset[Coord],
    ):
        self.dim = dim
        self.guard_direction = guard_direction
        self.guard_loc = guard_loc
        self.guard_location_history = guard_location_history
        self.obstruction_locs = obstruction_locs

    def __iter__(self):
        return self

    def __next__(self):
        next_guard_location = move(self.guard_loc, self.guard_direction)
        if out_of_bounds(next_guard_location, self.dim):
            raise StopIteration
        next_direction = self.guard_direction
        if next_guard_location in self.obstruction_locs:
            next_direction = turn_clockwise_90(self.guard_direction)
            next_guard_location = move(self.guard_loc, next_direction)
        next_guard_location_history = self.guard_location_history + [
            next_guard_location
        ]

        new_map = Map(
            dim=self.dim,
            guard_loc=next_guard_location,
            guard_direction=next_direction,
            guard_location_history=next_guard_location_history,
            obstruction_locs=self.obstruction_locs,
        )
        self.__dict__.update(new_map.__dict__)
        return new_map


def out_of_bounds(coord: Coord, dim: tuple[int, int]):
    x, y = coord
    x_dim, y_dim = dim
    return (x < 0 or x >= x_dim) or (y < 0 or y >= y_dim)


def move(coord: Coord, direction: Direction) -> Coord:
    x, y = coord
    match direction:
        case "up":
            return x, y - 1
        case "down":
            return x, y + 1
        case "right":
            return x + 1, y
        case "left":
            return x - 1, y


if __name__ == "__main__":
    with open("map.txt", "r") as file:
        map_ = Map.from_(file.read())

    *_, last = map_
    print(len(frozenset(last.guard_location_history)))
