import fileinput
import re

# regex = r'mul\((?P<first>\d+),(?P<second>\d+)\)'

# total = 0

# for line in fileinput.input():
#     for match in re.finditer(regex, line.strip(), re.MULTILINE):
#         print(match.group('first'))
#         total += int(match.group('first')) * int(match.group('second'))

# print(f"Part 1: {total}")


regex2 = r"(((?P<mul>mul)\((?P<first>\d+),(?P<second>\d+))\)|(?P<do>do\(\))|(?P<not>don't\(\)))"

do = True
total = 0

for line in fileinput.input():
    for match in re.finditer(regex2, line.strip(), re.MULTILINE):
        if match["do"]:
            do = True
        elif match["not"]:
            do = False
        elif match["mul"] and do:
            total += int(match.group("first")) * int(match.group("second"))

print(f"Part 2: {total}")
