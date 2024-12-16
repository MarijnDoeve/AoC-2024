import fileinput
from collections import defaultdict
from dataclasses import KW_ONLY, dataclass
from enum import Enum
from functools import cache
from typing import ClassVar, Self

type Point = tuple[int, int]


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


@dataclass()
class Node:
    grid: ClassVar[list[list[Self]]] = []
    y: int
    x: int
    _: KW_ONLY
    is_wall: bool = False

    @cache
    def neighbour(self, direction: Direction) -> Self | None:
        match direction:
            case direction.NORTH:
                return self._find_neighbour(0, -1)
            case direction.EAST:
                return self._find_neighbour(1, 0)
            case direction.SOUTH:
                return self._find_neighbour(0, 1)
            case direction.WEST:
                return self._find_neighbour(-1, 0)

        assert False

    def _find_neighbour(self, dy: int, dx: int) -> Self | None:
        if not self._in_grid(self.y + dy, self.x + dx):
            return None

        neighbor = self.grid[self.y + dy][self.x + dx]

        if neighbor.is_wall:
            return None
        return neighbor

    @classmethod
    def _in_grid(cls, y: int, x: int) -> bool:
        return y > 0 and x > 0 and y < len(cls.grid) and x < len(cls.grid[0])

    @classmethod
    def print_grid(cls):
        for line in cls.grid:
            print("".join("#" if tile.is_wall else "." for tile in line))

    def __hash__(self) -> int:
        return id(self)


if __name__ == "__main__":
    start = (0, 0)
    end = (0, 0)

    for y, line in enumerate(fileinput.input()):
        grid_line = []
        for x, char in enumerate(list(line.strip())):
            grid_line.append(Node(y, x, is_wall=char == "#"))
            if char == "S":
                start = (y, x)
            elif char == "E":
                end = (y, x)

        Node.grid.append(grid_line)

    assert start != (0, 0) and end != (0, 0)

    visited: defaultdict[Node, int] = defaultdict(lambda: 1_000_000)
    stack: list[tuple[Node, Direction, int]] = [
        (Node.grid[start[0]][start[1]], Direction.EAST, 0)
    ]

    while stack:
        current, current_direction, current_cost = stack.pop()

        for direction in Direction:
            if not (neighbor := current.neighbour(direction)):
                continue

            new_cost = current_cost + (1 if current_direction == direction else 1001)
            if new_cost >= visited[neighbor]:
                continue

            stack.append((neighbor, direction, new_cost))
            visited[neighbor] = new_cost

    print(visited[Node.grid[end[0]][end[1]]])
