import fileinput

MIN = 1
MAX = 3

reports: list[list[int]] = []

for line in fileinput.input():
    levels = [int(x) for x in line.strip().split()]
    reports.append(levels)


def safe_checker(levels: list[int]) -> bool:
    if levels != sorted(levels) and levels != sorted(levels, reverse=True):
        return False
    for i in range(len(levels) - 1):
        diff = abs(levels[i] - levels[i + 1])
        if diff < MIN or diff > MAX:
            return False
    return True


count = sum(safe_checker(levels) for levels in reports)

print(f"Part 1: {count}")

# part 2

count = 0

for levels in reports:
    if safe_checker(levels):
        count += 1
        continue

    for i in range(len(levels)):
        levels_cpy = levels.copy()
        levels_cpy.pop(i)
        if safe_checker(levels_cpy):
            count += 1
            break

print(f"Part 2: {count}")
