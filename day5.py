from collections import defaultdict
from fileinput import FileInput, input
from typing import Self


class UpdateNumber:
    page_rules: defaultdict[int, set[int]] = defaultdict(set)

    def __init__(self, number: int) -> None:
        self.number = number

    def __lt__(self, other: Self) -> bool:
        return other.number in UpdateNumber.page_rules[self.number]


class Day5:
    def __init__(self, reader: FileInput[str]) -> None:
        for line in reader:
            if line == "\n":
                break
            x, y = (int(x) for x in line.strip().split("|"))
            UpdateNumber.page_rules[x].add(y)

        updates = [
            [UpdateNumber(int(x)) for x in line.strip().split(",")] for line in reader
        ]

        total1 = total2 = 0
        for update in updates:
            if (update_sorted := sorted(update)) == update:
                total1 += update[len(update) // 2].number
                continue
            total2 += update_sorted[len(update) // 2].number

        print(f"Part 1: {total1}")
        print(f"Part 2: {total2}")


if __name__ == "__main__":
    Day5(input())
