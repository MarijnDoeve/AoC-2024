from copy import deepcopy
import fileinput

GridType = list[list["Position"]]
Pos = tuple[int, int]


class Position:
    def __init__(self, obstacle: bool) -> None:
        self.visited = False
        self.obstacle = obstacle
        self.visited_direction: set[int] = set()


class Day6:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, input: fileinput.FileInput[str]) -> None:
        self.grid: GridType = []

        direction, guard = self.load_input(input)

        self.part1(direction, guard)
        self.part2()

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
        while True:
            y, x = guard
            current = self.grid[y][x]
            current.visited = True
            current.visited_direction.add(direction)
            y_next, x_next = self.next_pos(y, x, direction)

            if not self.in_grid(y_next, x_next):
                break

            if self.grid[y_next][x_next].obstacle == True:
                direction = (direction + 1) % 4
                y_next, x_next = self.next_pos(y, x, direction)

            guard = (y_next, x_next)

        total = sum([sum([pos.visited for pos in line]) for line in self.grid])

        # self.print_grid(self.grid)
        print(f"Part 1: {total}")

    def part2(self) -> None:
        total = 0

        for line in self.grid:
            for pos in line:
                if pos.obstacle:
                    continue
                # Change to obstacle, check for loops
                copy_grid = deepcopy(self.grid)

        print(f"Part 2: {total}")

    def has_loops(self, grid: GridType) -> bool:
        return False

    def print_grid(self, grid: GridType) -> None:
        for line in grid:
            for pos in line:
                if pos.obstacle:
                    print("#", end="")
                elif pos.visited:
                    print("X", end="")
                else:
                    print(".", end="")
            print()

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

    def in_grid(self, y: int, x: int) -> bool:
        return x >= 0 and x < len(self.grid[0]) and y >= 0 and y < len(self.grid)


if __name__ == "__main__":
    Day6(fileinput.input())
