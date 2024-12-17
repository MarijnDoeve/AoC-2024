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
    def print_grid(cls, marked_nodes=None):
        if marked_nodes is None:
            marked_nodes = set()
        for line in cls.grid:
            print(
                "".join(
                    "#" if tile.is_wall else "O" if tile in marked_nodes else "."
                    for tile in line
                )
            )

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

    start_node = Node.grid[start[0]][start[1]]

    visited: defaultdict[tuple[int, int, Direction], int] = defaultdict(
        lambda: 1_000_000
    )
    queue: list[tuple[Node, Direction, int, list[Node]]] = [
        (start_node, Direction.EAST, 0, [start_node])
    ]

    full_paths: list[tuple[int, list[Node]]] = []
    while queue:
        current, current_direction, current_cost, current_path = queue.pop(0)

        for direction in Direction:
            if not (neighbor := current.neighbour(direction)):
                continue

            new_cost = current_cost + (1 if current_direction == direction else 1001)
            if new_cost > visited[(neighbor.y, neighbor.x, direction)]:
                continue

            visited[(neighbor.y, neighbor.x, direction)] = new_cost

            if (neighbor.y, neighbor.x) == end:
                full_paths.append((new_cost, current_path + [neighbor]))
                continue

            queue.append((neighbor, direction, new_cost, current_path + [neighbor]))

    lowest_cost = min(visited[(end[0], end[1], dir)] for dir in Direction)

    print(f"Part 1: {lowest_cost}")

    best_seats: set[Node] = set()

    for cost, node_list in full_paths:
        if cost != lowest_cost:
            continue

        best_seats.update(node_list)
    Node.print_grid(best_seats)

    print(f"Part 2: {len(best_seats)}")
