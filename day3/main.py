from pathlib import Path
import re

FILE_DIR = Path(__file__).parent.absolute()
MUL_RE = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
DO_MUL_RE = re.compile(r"(don't|do|mul)\((\d{0,3}),{0,1}(\d{0,3})\)")


def get_input() -> list[str]:
    with open(FILE_DIR / "input.txt", "r") as f:
        lines = f.readlines()
    return lines


def parse_input(lines: list[str]) -> list[list[int]]:
    return [list(map(int, line.split())) for line in lines]


def part1(lines: list[str]) -> int:
    total = 0
    for line in lines:
        for match in MUL_RE.finditer(line):
            groups = list(map(int, match.groups()))
            total += groups[0] * groups[1]
    return total


def part2(lines: list[str]) -> int:
    total = 0
    ignore_mul = False
    for line in lines:
        for match in DO_MUL_RE.finditer(line):
            groups = match.groups()
            match groups[0]:
                case "do":
                    ignore_mul = False
                case "don't":
                    ignore_mul = True
                case "mul":
                    if ignore_mul:
                        continue

                    total += int(groups[1]) * int(groups[2])
    return total


if __name__ == "__main__":
    input_str = get_input()
    print(part1(input_str))
    print(part2(input_str))
