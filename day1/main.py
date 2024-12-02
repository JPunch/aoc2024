from pathlib import Path
from functools import reduce
from collections import Counter

FILE_DIR = Path(__file__).parent.absolute()


def get_input() -> list[str]:
    with open(FILE_DIR / "input.txt", "r") as f:
        lines = f.readlines()
    return lines


def parse_input(lines: list[str]) -> tuple[list[int], list[int]]:
    list1 = []
    list2 = []
    for line in lines:
        x, y = line.split()
        list1.append(int(x))
        list2.append(int(y))
    return list1, list2


def part1(lists: tuple[list[int], list[int]]) -> int:
    sorted_lists = [sorted(lst) for lst in lists]
    return sum(abs(x - y) for x, y in zip(*sorted_lists))


def part2(lists: tuple[list[int], list[int]]):
    list2_counter = Counter(lists[1])
    total = 0
    for i in lists[0]:
        total += i * list2_counter.get(i, 0)
    return total


if __name__ == "__main__":
    input_str = get_input()
    parsed = parse_input(input_str)
    print(part1(parsed))
    print(part2(parsed))
