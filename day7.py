import fileinput
from itertools import product
from math import ceil, log10
from operator import add, mul
from typing import Callable, Iterable

OPERATIONS1 = [add, mul]

concat: Callable[[int, int], int] = lambda a, b: int(str(a) + str(b))
OPERATIONS2 = OPERATIONS1 + [concat]


def gives_answer(
    answer: int, numbers: list[int], operations: Iterable[Callable[[int, int], int]]
) -> bool:
    total = numbers[0]
    for i, operation in enumerate(operations):
        total = operation(total, numbers[i + 1])
        if total > answer:
            return False

    return total == answer


total1 = 0
total2 = 0

for line in fileinput.input():
    answer_str, numbers_str = line.strip().split(":")
    numbers = [int(x) for x in numbers_str.split()]
    answer = int(answer_str)

    for operations in product(OPERATIONS1, repeat=len(numbers) - 1):
        if gives_answer(answer, numbers, operations):
            total1 += answer
            break

    for operations in product(OPERATIONS2, repeat=len(numbers) - 1):
        if gives_answer(answer, numbers, operations):
            total2 += answer
            break

print(f"Part 1: {total1}")
print(f"Part 2: {total2}")
