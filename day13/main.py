from pathlib import Path
from enum import auto, Enum
from collections import defaultdict

FILE_DIR = Path(__file__).parent.absolute()


def get_input() -> list[str]:
    with open(FILE_DIR / "test_input.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines

def parse_input(data: list[str]):
    entries = []
    for i in range(0, len(data), 3):
        a = data[i]
        b = data[i+1]
        g = data[i+2]
        a = a.split()
        b = b.split()
        g = g.split()
        a = (int(a[2][2:-1]), int(a[3][2:]))
        b = (int(b[2][2:-1]), int(b[3][2:]))
        g = (int(g[1][2:-1]), int(g[2][2:]))
        entries.append([a, b, g])
    return entries

def part1(entries: list) -> int:
    return 0


def part2(entries: list) -> int:
    return 0


if __name__ == "__main__":
    input_strs = get_input()
    parsed = parse_input(input_strs)
    print(part1(parsed))
    print(part2(parsed))
