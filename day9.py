import fileinput


class Day9:
    class IterationDoneException(Exception):
        pass

    def __init__(self) -> None:
        self.fs1: list[str] = []

        line = fileinput.input().readline()
        for i, char in enumerate(list(line)):
            self.fs1 += ["." if i % 2 else str(i // 2)] * int(char)

        self.fs2 = self.fs1.copy()

        self.front_pointer = -1
        self.back_pointer = len(self.fs1)
        self.part1()
        self.last_filename = 10_000
        self.part2()

    def part1(self) -> None:
        try:
            while True:
                self.front_pointer += 1

                num = self.fs1[self.front_pointer]
                if num != ".":
                    continue

                self.fs1[self.front_pointer] = self.get_block_from_back()

        except Day9.IterationDoneException:
            pass
        finally:
            print(f"Part 1: {self.calculate_checksum(self.fs1)}")

    def get_block_from_back(self) -> str:
        while True:
            self.back_pointer -= 1
            if self.back_pointer <= self.front_pointer:
                raise Day9.IterationDoneException

            if (value := self.fs1[self.back_pointer]) == ".":
                continue

            self.fs1[self.back_pointer] = "."
            return value

    def part2(self) -> None:
        self.back_pointer = len(self.fs1)
        while True:
            try:
                name, length, old_pos = self.get_file_from_back()
            except Day9.IterationDoneException:
                break

            # Find space
            found_length = 0
            start_pos = -1
            for i, block in enumerate(self.fs2):
                if block != ".":
                    found_length = 0
                    start_pos = -1
                    continue

                if found_length == 0:
                    start_pos = i

                found_length += 1
                if found_length == length:
                    break

            if start_pos == -1 or found_length != length or old_pos < start_pos:
                continue

            # Move file
            for i in range(length):
                self.fs2[start_pos + i] = name
                self.fs2[old_pos + i] = "."

        print(f"Part 2: {self.calculate_checksum(self.fs2)}")

    def get_file_from_back(self) -> tuple[str, int, int]:
        while True:
            self.back_pointer -= 1
            if self.back_pointer < 0:
                raise Day9.IterationDoneException

            block = self.fs2[self.back_pointer]
            if block == ".":
                continue
            if int(block) > self.last_filename:
                raise Day9.IterationDoneException

            file_length = 1
            try:
                while True:
                    if block != self.fs2[self.back_pointer - 1]:
                        break
                    self.back_pointer -= 1

                    file_length += 1
            except IndexError:
                pass

            return (block, file_length, self.back_pointer)

    def calculate_checksum(self, fs: list[str]) -> int:
        return sum(i * int(value) if value != "." else 0 for i, value in enumerate(fs))


if __name__ == "__main__":
    Day9()
