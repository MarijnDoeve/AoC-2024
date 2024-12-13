import fileinput
from os import stat
import networkx as nx
from functools import cache
from typing import Generator, Self

Point = tuple[int, int]


class Plot:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, position: Point, plant_type: str) -> None:
        self.fences: list[bool] = [False for _ in range(4)]

        self.position: Point = position
        self.plant_type: str = plant_type

    @property
    def y(self) -> int:
        return self.position[0]

    @property
    def x(self) -> int:
        return self.position[1]

    def __repr__(self) -> str:
        return f"({self.y}, {self.x}) {self.plant_type}, {self.fences}"


class Day12:
    def __init__(self, grid: dict[Point, Plot], max_y: int, max_x: int) -> None:
        self.grid: dict[Point, Plot] = grid
        self.max_y: int = max_y
        self.max_x: int = max_x

        self.regions: list[set[Plot]] = []

        self.place_fences()
        self.grid_to_graph()

        print(f"Part 1: {self.calculate_price1()}")
        print(f"Part 2: {self.calculate_bulk_price()}")

    # can be skipped for the connectivity of a plot
    def place_fences(self) -> None:
        for x in range(self.max_x + 1):
            self.grid[(0, x)].fences[Plot.UP] = True
        for y in range(self.max_y + 1):
            self.grid[(y, 0)].fences[Plot.LEFT] = True
        for x in range(self.max_x + 1):
            self.grid[(self.max_y, x)].fences[Plot.DOWN] = True

        for y in range(self.max_y + 1):
            self.grid[(y, self.max_x)].fences[Plot.RIGHT] = True

        for _, plot in self.grid.items():
            for direction, neighbour in self.get_neighbour(plot):
                if neighbour.plant_type != plot.plant_type:
                    plot.fences[direction] = True

    def grid_to_graph(self) -> None:
        graph = nx.Graph()
        graph.add_nodes_from(self.grid.values())
        for plot in self.grid.values():
            for _, neighbour in self.get_neighbour(plot):
                if plot.plant_type != neighbour.plant_type:
                    continue
                graph.add_edge(plot, neighbour)

        self.regions = list(nx.connected_components(graph))

    def calculate_price1(self) -> int:
        price = 0
        for region in self.regions:
            fences = sum(sum(plot.fences) for plot in region)
            n_plots = len(region)
            price += fences * n_plots
            # print(
            #     f"A region of {region.pop().plant_type} plants with price {n_plots} * {fences} = {n_plots * fences}"
            # )

        return price

    def calculate_bulk_price(self) -> int:
        total = 0
        for region in self.regions:
            sides = self.get_corners(region)
            n_plots = len(region)
            total += sides * n_plots
            print(
                f"A region of {region.pop().plant_type} plants with price {n_plots} * {sides} = {n_plots * sides}"
            )
        return total

    def get_corners(self, region: set[Plot]) -> int:
        n_corners = 0
        for plot in region:
            match len(plot.fences):
                case 0:
                    n_corners += self.count_diagonal_other_types(plot)
                case 1:
                    diag = self.count_diagonal_other_types(plot)
                    if diag == 4:
                        n_corners += 2
                    elif 3:
                        n_corners
                case 2:
                    if plot.fences == [
                        True,
                        False,
                        True,
                        False,
                    ] or plot.fences == [
                        False,
                        True,
                        False,
                        True,
                    ]:
                        break
                    n_corners += self.count_diagonal_other_types(plot)
                case 3:
                    n_corners += 2
                case 4:
                    n_corners += 4

        return n_corners

    def count_diagonal_other_types(self, plot: Plot) -> int:
        count = 0

        for dy, dx in [(-1, -1), (+1, +1), (+1, -1), (-1, +1)]:
            if not self.in_grid(plot.y + dy, plot.x + dx):
                continue

            if self.grid[(plot.y + dy, plot.x + dx)].plant_type == plot.plant_type:
                continue

            count += 1

        return count

    def get_neighbour(self, plot: Plot) -> Generator[tuple[int, Plot]]:
        for direction, (dy, dx) in enumerate(((-1, 0), (0, +1), (+1, 0), (0, -1))):
            if not self.in_grid(plot.y + dy, plot.x + dx):
                continue

            yield direction, self.grid[(plot.y + dy, plot.x + dx)]

    @cache
    def in_grid(self, y: int, x: int) -> bool:
        return y >= 0 and y <= self.max_y and x >= 0 and x <= self.max_x

    @classmethod
    def read_input(cls) -> Self:
        grid = {}

        for y, line in enumerate(fileinput.input()):
            for x, plant_type in enumerate(list(line.strip())):
                grid[(y, x)] = Plot((y, x), plant_type)

        return cls(grid, y, x)


if __name__ == "__main__":
    day12: Day12 = Day12.read_input()
