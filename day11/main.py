from pathlib import Path
from functools import cache

FILE_DIR = Path(__file__).parent.absolute()


def get_input() -> list[str]:
    with open(FILE_DIR / "input.txt", "r") as f:
        data = f.read()
    return [int(x) for x in data.strip().split()]


@cache
def blink(val: int, times_left: int) -> int:
    if times_left == 0:
        stones = 1
    elif val == 0:
        stones = blink(1, times_left - 1)
    elif len(str(val)) % 2 == 0:
        middle_index = len(str(val)) // 2
        left = int(str(val)[:middle_index])
        right = int(str(val)[middle_index:])
        stones = blink(left, times_left - 1) + blink(right, times_left - 1)
    else:
        stones = blink(val * 2024, times_left - 1)
    return stones


def part1(i_arrangement: list[int]):
    return sum([blink(stone, 25) for stone in i_arrangement])


def part2(i_arrangement: list[int]) -> int:
    return sum([blink(stone, 75) for stone in i_arrangement])


if __name__ == "__main__":
    input_str = get_input()
    print(input_str)
    print(part1(input_str))
    print(part2(input_str))
