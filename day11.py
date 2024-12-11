import fileinput
from collections import defaultdict

stone_map: defaultdict[int, int] = defaultdict(int)

for stone in [int(x) for x in fileinput.input().readline().strip().split()]:
    stone_map[stone] += 1

for i in range(75):
    if i == 25:
        print(f"Part 1: {sum(stone_map.values())}")

    new_stones: defaultdict[int, int] = defaultdict(int)

    for stone, n in stone_map.items():
        if stone == 0:
            new_stones[1] += n
        elif (stone_len := len((stone_str := str(stone)))) % 2 == 0:
            new_stones[int(stone_str[: (stone_len // 2)])] += n
            new_stones[int(stone_str[stone_len // 2 :])] += n
        else:
            new_stones[stone * 2024] += n

    stone_map = new_stones

print(f"Part 2: {sum(stone_map.values())}")
