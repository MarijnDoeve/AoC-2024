import fileinput

Point = tuple[int, int]
Trail = tuple[Point, ...]

grid = [[int(x) for x in list(line.strip())] for line in fileinput.input()]


stack: list[Trail] = []
for y, line in enumerate(grid):
    for x, number in enumerate(line):
        if number != 0:
            continue

        stack.append(((y, x),))


def find_neighbors(grid: list[list[int]], y: int, x: int, height: int) -> list[Point]:
    neighbors = []
    for dy, dx in [(+1, 0), (0, +1), (-1, 0), (0, -1)]:
        new_y = y + dy
        new_x = x + dx
        if new_y < 0 or new_x < 0 or new_y >= len(grid) or new_x >= len(grid[0]):
            continue

        if grid[new_y][new_x] == height:
            neighbors.append((new_y, new_x))

    return neighbors


finished_trails = set()
distinct_trails = set()
while stack:
    current = stack.pop()
    if len(current) == 10:
        distinct_trails.add(current)
        finished_trails.add((current[0], current[-1]))

    for neighbor in find_neighbors(grid, *current[-1], len(current)):
        stack.append(current + (neighbor,))

print(f"Part 1: {len(finished_trails)}")
print(f"Part 2: {len(distinct_trails)}")
