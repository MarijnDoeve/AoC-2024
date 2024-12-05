from collections import defaultdict
from fileinput import FileInput
from typing import Self


class Day5:
    class UpdateNumber:
        def __init__(self, number: int, rules: set[int]) -> None:
            self.number = number
            self.rules = rules

        def __lt__(self, other: Self) -> bool:
            return other.number in self.rules

    def __init__(self, reader: FileInput[str]) -> None:
        self.page_rules: defaultdict[int, set[int]] = defaultdict(set)
        self.total2 = 0

        for line in reader:
            if line == "\n":
                break
            x, y = (int(x) for x in line.strip().split("|"))
            self.page_rules[x].add(y)

        updates = []

        for line in reader:
            updates.append([int(x) for x in line.strip().split(",")])

        total1 = 0
        total2 = 0
        for update in updates:
            result = self.check_list(update)
            if result > 0:
                total1 += result
                continue

            total2 += sorted(
                [self.UpdateNumber(x, self.page_rules[x]) for x in update]
            )[len(update) // 2].number

        print(f"Part 1: {total1}")
        print(f"Part 2: {total2}")

    def check_list(self, update: list[int]) -> int:
        for i, number in enumerate(update):
            if number not in self.page_rules:
                continue

            if self.page_rules[number].intersection(update[:i]):
                return 0

        return update[len(update) // 2]


if __name__ == "__main__":
    import fileinput

    Day5(fileinput.input())
