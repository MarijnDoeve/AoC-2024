import fileinput
from copy import deepcopy
from typing import Self

GridType = list[list["Position"]]
Pos = tuple[int, int]


class LoopDetectedException(Exception):
    pass


class Position:
    def __init__(self, obstacle: bool) -> None:
        self.visited = False
        self.obstacle = obstacle
        self.visited_direction: set[int] = set()

    def __copy__(self) -> "Position":
        return Position(self.obstacle)

    def __deepcopy__(self, memo: dict[int, Self]) -> "Position":
        return self.__copy__()


class Day6:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, input: fileinput.FileInput[str]) -> None:
        self.grid: GridType = []
        direction, guard = self.load_input(input)
        self.part2(direction, deepcopy(guard))

    def load_input(self, input: fileinput.FileInput[str]) -> tuple[int, Pos]:
        direction: int = Day6.UP
        guard = (0, 0)

        for y, line in enumerate(input):
            grid_line = []
            for x, char in enumerate(line.strip()):
                grid_line.append(Position(char == "#"))
                if char == "^":
                    guard = (y, x)
                    grid_line[-1].visited = True
            self.grid.append(grid_line)

        return direction, guard

    def part1(self, direction: int, guard: Pos) -> None:
        grid = deepcopy(self.grid)
        self.walk_grid(direction, guard, grid)
        total = sum([sum([pos.visited for pos in line]) for line in grid])

        print(f"Part 1: {total}")

    @staticmethod
    def walk_grid(
        direction: int,
        guard: Pos,
        grid: GridType,
        detect_loops: bool = True,
    ) -> None:
        while True:
            y, x = guard
            current = grid[y][x]

            if detect_loops and direction in current.visited_direction:
                raise LoopDetectedException

            current.visited = True
            current.visited_direction.add(direction)
            y_next, x_next = Day6.next_pos(y, x, direction)

            if not Day6.in_grid(y_next, x_next, grid):
                break

            if grid[y_next][x_next].obstacle == True:
                direction = (direction + 1) % 4
                continue

            guard = (y_next, x_next)

    def part2(self, direction: int, guard: Pos) -> None:
        total = 0
        progress = 0
        out_of = len(self.grid) * len(self.grid[0])
        space = len(str(out_of))

        for y, line in enumerate(self.grid):
            for x, pos in enumerate(line):
                progress += 1
                print(f"{progress:>{space}}/{out_of}")

                if pos.obstacle:
                    continue

                copy_grid = deepcopy(self.grid)
                copy_grid[y][x].obstacle = True
                try:
                    self.walk_grid(direction, deepcopy(guard), copy_grid)
                except LoopDetectedException:
                    total += 1

        print(f"Part 2: {total}")

    @staticmethod
    def next_pos(y: int, x: int, direction: int) -> Pos:
        match direction:
            case Day6.UP:
                return (y - 1, x)
            case Day6.RIGHT:
                return (y, x + 1)
            case Day6.DOWN:
                return (y + 1, x)
            case Day6.LEFT:
                return (y, x - 1)
            case _:
                raise ValueError

    @staticmethod
    def in_grid(y: int, x: int, grid: GridType) -> bool:
        return x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)


if __name__ == "__main__":
    Day6(fileinput.input())
