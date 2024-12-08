import fileinput
from collections import defaultdict
from itertools import combinations

Coordinate = tuple[int, int]

antennas: defaultdict[str, list[Coordinate]] = defaultdict(list)

for y, line in enumerate(fileinput.input()):
    for x, pos in enumerate(list(line.strip())):
        if pos == ".":
            continue

        antennas[pos].append((y, x))

max_y = y
max_x = x

antinodes1: set[Coordinate] = set()
antinodes2: set[Coordinate] = set()


for letter, nodes in antennas.items():
    pairs = combinations(nodes, 2)
    for (y0, x0), (y1, x1) in pairs:
        dy = y0 - y1
        dx = x0 - x1

        antinodes2.add((y0, x0))
        antinodes2.add((y1, x1))

        for old_y, old_x in (y0, x0), (y1, x1):
            for factor in (-1, +1):
                new_y = old_y + dy * factor
                new_x = old_x + dx * factor

                # Check if y or x between points
                if (new_y >= min(y0, y1) and new_y <= max(y0, y1)) or (
                    new_x >= min(x0, x1) and new_x <= max(x0, x1)
                ):
                    continue

                # check if out of bounds
                if new_y < 0 or new_y > max_y or new_x < 0 or new_x > max_x:
                    continue

                antinodes1.add((new_y, new_x))

                # calculate resonance
                while True:
                    new_y = new_y + dy * factor
                    new_x = new_x + dx * factor

                    if new_y < 0 or new_y > max_y or new_x < 0 or new_x > max_x:
                        break

                    antinodes2.add((new_y, new_x))

print(f"Part 1: {len(antinodes1)}")
print(f"Part 2: {len(antinodes1 | antinodes2)}")
