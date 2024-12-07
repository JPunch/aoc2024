from pathlib import Path

FILE_DIR = Path(__file__).parent.absolute()


def get_input() -> list[str]:
    with open(FILE_DIR / "input.txt", "r") as f:
        data = f.readlines()
    return data


def parse_data(lines: list[str]) -> list[tuple[int, tuple[int]]]:
    vals = []
    for line in lines:
        ans, r = line.strip().split(":")
        r = r.strip().split()
        vals.append((int(ans), tuple(map(int, r))))
    return vals


def part1(eqs: list[tuple[int]]) -> int:
    total = 0
    for ans, args in eqs:
        if recursion_part1(ans, args[0], args[1:]):
            total += ans
    return total


def recursion_part1(ans, curr, args):
    if len(args) == 0:
        if curr == ans:
            return True
        return False
    arg = args[0]
    if curr * arg <= ans:
        out = curr * arg
        if recursion_part1(ans, out, args[1:]):
            return True
    if recursion_part1(ans, curr + arg, args[1:]):
        return True


def recursion_part2(ans, curr, args):
    if len(args) == 0:
        if curr == ans:
            return True
        return False
    arg = args[0]
    if curr * arg <= ans:
        out = curr * arg
        if recursion_part2(ans, out, args[1:]):
            return True
    if recursion_part2(ans, curr + arg, args[1:]):
        return True
    if recursion_part2(ans, int(str(curr) + str(args[0])), args[1:]):
        return True


def part2(eqs: list[tuple[int]]) -> int:
    total = 0
    for ans, args in eqs:
        if recursion_part2(ans, args[0], args[1:]):
            total += ans
    return total


if __name__ == "__main__":
    input_str = get_input()
    eqs = parse_data(input_str)
    print(part1(eqs))
    print(part2(eqs))
