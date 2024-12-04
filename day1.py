import fileinput
from collections import defaultdict

lefts = []
rights = []

for line in fileinput.input():
    left, right = [int(x) for x in line.strip().split()]
    lefts.append(left)
    rights.append(right)

lefts.sort()
rights.sort()

assert len(lefts) == len(rights)

total = 0

for i in range(len(lefts)):
    total += abs(lefts[i] - rights[i])

print(f"Part 1: {total}")

# PART 2

counts: defaultdict[int, int] = defaultdict(int)

for number in rights:
    counts[number] += 1

total = 0

for number in lefts:
    total += number * counts[number]

print(f"Part 2: {total}")
