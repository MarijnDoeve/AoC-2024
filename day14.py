import fileinput
import re
from dataclasses import dataclass
from math import prod
from re import Match

Point = tuple[int, int]

WIDTH = 101
HEIGHT = 103
SECONDS = 100


@dataclass
class Robot:
    position: Point
    velocity: Point

    def step(self, stepsize=1) -> None:
        new_x = (robot.position[0] + robot.velocity[0] * stepsize) % WIDTH
        new_y = (robot.position[1] + robot.velocity[1] * stepsize) % HEIGHT
        robot.position = (new_x, new_y)


robots = []

regex = re.compile(r"^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$")
for line in fileinput.input():
    match = regex.match(line)
    assert type(match) == Match
    robots.append(
        Robot(
            (int(match.group(1)), int(match.group(2))),
            (int(match.group(3)), int(match.group(4))),
        )
    )

quadrants = [0, 0, 0, 0]

X_MID = WIDTH // 2
Y_MID = HEIGHT // 2

for robot in robots:
    robot.step(SECONDS)
    new_x, new_y = robot.position

    if new_x < X_MID and new_y < Y_MID:
        quadrants[0] += 1
    elif new_x > X_MID and new_y < Y_MID:
        quadrants[1] += 1
    elif new_x < X_MID and new_y > Y_MID:
        quadrants[2] += 1
    elif new_x > X_MID and new_y > Y_MID:
        quadrants[3] += 1

total = prod(quadrants)
print(f"Part 1: {total}")

seconds = 100

while True:
    grid = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for robot in robots:
        robot.step()
        grid[robot.position[1]][robot.position[0]] = "#"

    seconds += 1
    for line in grid:
        if "".join(line).find("####################") != -1:
            for line in grid:
                print("".join(line))
            print(f"Part 1: {total}")
            print(f"Part 2: {seconds}")
            exit()
