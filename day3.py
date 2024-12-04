import fileinput
import re

lines = "".join(line.strip() for line in fileinput.input())

# Part 1

regex = r"mul\((?P<first>\d+),(?P<second>\d+)\)"
total = 0

for match in re.finditer(regex, lines):
    total += int(match.group("first")) * int(match.group("second"))

print(f"Part 1: {total}")

# Part 2

regex = r"mul\((?P<first>\d+),(?P<second>\d+)\)|(?P<do>do\(\))|(?P<not>don't\(\))"
do = True
total = 0
for match in re.finditer(regex, lines):
    if match["do"]:
        do = True
    elif match["not"]:
        do = False
    elif do:
        total += int(match.group("first")) * int(match.group("second"))

print(f"Part 2: {total}")
