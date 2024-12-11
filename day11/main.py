from pathlib import Path
from enum import auto, Enum

FILE_DIR = Path(__file__).parent.absolute()


def get_input() -> list[str]:
    with open(FILE_DIR / "input.txt", "r") as f:
        data = f.read()
    return [int(x) for x in data.strip().split()]


# 0 -> 1
# if even num of digits split in half e.g. 1000 -> 10, 0
# otherwise times by 2024


def part1(i_arrangement: list[int]) -> int:
    stones = i_arrangement.copy()
    for _ in range(25):
        new_stones = []
        for i in stones:
            if i == 0:
                new_stones.append(1)
            elif not len(str(i)) % 2:
                middle_index = len(str(i)) // 2
                left = int(str(i)[:middle_index])
                right = int(str(i)[middle_index:])
                new_stones.append(left)
                new_stones.append(right)
            else:
                new_stones.append(2024 * i)
        stones = new_stones.copy()
    return len(stones)


def part2(i_arrangement: list[int]) -> int:
    stones = i_arrangement.copy()
    for _ in range(75):
        new_stones = []
        for i in stones:
            if i == 0:
                new_stones.append(1)
            elif not len(str(i)) % 2:
                middle_index = len(str(i)) // 2
                left = int(str(i)[:middle_index])
                right = int(str(i)[middle_index:])
                new_stones.append(left)
                new_stones.append(right)
            else:
                new_stones.append(2024 * i)
        stones = new_stones.copy()
    return len(stones)


if __name__ == "__main__":
    input_str = get_input()
    print(input_str)
    print(part1(input_str))
    print(part2(input_str))
