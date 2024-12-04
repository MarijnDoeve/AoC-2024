import fileinput
import re

horizontal = [line.strip() for line in fileinput.input()]
vertical = list(map(lambda x: "".join(x), zip(*horizontal)))

grid = [list(line) for line in horizontal]


def diagonal_for_start_lr(start_y: int, start_x: int, grid: list[list[str]]) -> str:
    return "".join(
        grid[y][x]
        for y, x in zip(range(start_y, len(grid)), range(start_x, len(grid[0])))
    )


diagonal_lr = [
    diagonal_for_start_lr(y, x, grid)
    for (y, x) in [(0, x) for x in range(0, len(grid[0]))]
    + [(y, 0) for y in range(1, len(grid))]
]


def diagonal_for_start_rl(start_y: int, start_x: int, grid: list[list[str]]) -> str:
    return "".join(
        grid[y][x] for y, x in zip(range(start_y, len(grid)), range(start_x, -1, -1))
    )


diagonal_rl = [
    diagonal_for_start_rl(y, x, grid)
    for (y, x) in [(0, x) for x in range(0, len(grid[0]))]
    + [(y, len(grid[0]) - 1) for y in range(1, len(grid))]
]

all = horizontal + vertical + diagonal_lr + diagonal_rl

assert (
    len("".join(horizontal))
    == len("".join(vertical))
    == len("".join(diagonal_lr))
    == len("".join(diagonal_rl))
)

total = sum(len(re.findall(r"(?=(XMAS|SAMX))", line)) for line in all)

print(f"Part 1: {total}")

MAS = {"MAS", "SAM"}

total = 0
for y in range(1, len(grid) - 1):
    for x in range(1, len(grid[0]) - 1):
        if grid[y][x] != "A":
            continue

        if (grid[y - 1][x - 1] + "A" + grid[y + 1][x + 1]) in MAS and (
            grid[y - 1][x + 1] + "A" + grid[y + 1][x - 1]
        ) in MAS:
            total += 1

print(f"Part 2: {total}")
