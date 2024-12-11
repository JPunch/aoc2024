from pathlib import Path
from functools import cache
from collections import defaultdict

FILE_DIR = Path(__file__).parent.absolute()


def get_input() -> list[str]:
    with open(FILE_DIR / "input.txt", "r") as f:
        data = f.read()
    return [int(x) for x in data.strip().split()]


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


@cache
def blink25(val: int) -> list[int]:
    stones = [val]
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
    return stones


def part2(i_arrangement: list[int]) -> int:
    stone_dict = defaultdict(int)
    temp_dict = defaultdict(int)
    for stone in i_arrangement:
        stone_dict[stone] += 1
    for _ in range(3):
        for key, val in stone_dict.items():
            new_stones = blink25(key)
            for stone in new_stones:
                temp_dict[stone] += 1 * val
        stone_dict = temp_dict
        temp_dict = defaultdict(int)
    return sum(stone_dict.values())


if __name__ == "__main__":
    input_str = get_input()
    print(input_str)
    print(part1(input_str))
    print(part2(input_str))
