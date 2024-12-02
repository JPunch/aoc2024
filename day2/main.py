from pathlib import Path
import numpy as np

FILE_DIR = Path(__file__).parent.absolute()


def get_input() -> list[str]:
    with open(FILE_DIR / "input.txt", "r") as f:
        lines = f.readlines()
    return lines


def parse_input(lines: list[str]) -> list[list[int]]:
    return [list(map(int, line.split())) for line in lines]


def check_report(report: list[int], part2: bool = False) -> bool:
    diff = np.diff(report)
    if (np.all(diff > 0) or np.all(diff < 0)) and max(np.abs(diff)) <= 3:  # all increase or decrease
        return True
    if part2:
        for x in range(len(report)):
            # construct combinations of report
            new = report[:x] + report[x + 1 :]
            if check_report(new):
                return True
    return False


def part1(reports: list[list[int]]) -> int:
    return [check_report(report) for report in reports].count(True)


def part2(reports: list[list[int]]) -> int:
    return [check_report(report, True) for report in reports].count(True)


if __name__ == "__main__":
    input_str = get_input()
    parsed = parse_input(input_str)
    print(part1(parsed))
    print(part2(parsed))
