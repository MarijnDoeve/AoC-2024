import fileinput
import re
from dataclasses import dataclass
from functools import cache
from re import Match

Point = tuple[int, int]


@dataclass
class ClawMachine:
    button_a: Point
    button_b: Point
    prize: Point

    def part_2(self) -> None:
        self.prize = (
            self.prize[0] + 10_000_000_000_000,
            self.prize[1] + 10_000_000_000_000,
        )

    def solve_with_linalg(self) -> int:
        ax, ay = self.button_a
        bx, by = self.button_b
        px, py = self.prize

        f = 1 / (ax * by - bx * ay)

        na = round(px * (f * by) + py * (f * bx * -1))
        nb = round(px * (f * ay * -1) + py * (f * ax))

        return na * 3 + nb if na * ax + nb * bx == px and na * ay + nb * by == py else 0

    def find_cheapest_path(self) -> int:
        visited: set[Point] = set()
        stack = [(0, 0)]
        cheapest = 1_000_000

        while stack:
            a, b = stack.pop()

            if (a, b) in visited:
                continue

            visited.add((a, b))

            x, y = self._get_location(a, b)

            if x > self.prize[0] or y > self.prize[1]:
                continue

            if self.prize == (x, y):
                cost = a * 3 + b
                if cost < cheapest:
                    cheapest = cost

            stack.append((a + 1, b))
            stack.append((a, b + 1))

        return cheapest if cheapest < 1_000_000 else 0

    @cache
    def _get_location(self, a: int, b: int) -> Point:
        return (
            a * self.button_a[0] + b * self.button_b[0],
            a * self.button_a[1] + b * self.button_b[1],
        )

    def __hash__(self) -> int:
        return id(self)


machines = []

regex = re.compile(r"^\w+ ?\w?: X[+=](\d+), Y[+=](\d+)$")

read_stack: list[tuple[int, int]] = []
for line in fileinput.input():
    if line == "\n":
        machines.append(ClawMachine(*read_stack))
        read_stack = []
        continue

    match = regex.match(line)
    assert type(match) == Match
    read_stack.append((int(match.group(1)), int(match.group(2))))

machines.append(ClawMachine(*read_stack))

total = sum(machine.solve_with_linalg() for machine in machines)

print(f"Part 1: {total}")

for machine in machines:
    machine.part_2()

total = sum(machine.solve_with_linalg() for machine in machines)

print(f"Part 2: {total}")
