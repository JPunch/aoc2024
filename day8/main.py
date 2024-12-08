from pathlib import Path
from pprint import pp
import typing as t
from collections import defaultdict
from itertools import combinations

FILE_DIR = Path(__file__).parent.absolute()
GRID = []


def get_input() -> list[str]:
    with open(FILE_DIR / "input.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


class Grid:
    def __init__(self, rows: list[str]):
        self.rows = rows
        self.width = len(rows[0])
        self.height = len(rows)
        self.antinodes = set()

    def reset(self):
        self.antinodes = set()

    def in_grid(self, row: int, column: int) -> bool:
        return (0 <= row <= self.height - 1) and (0 <= column <= self.width - 1)


coord_diff = lambda x, y: (x[0] - y[0], x[1] - y[1])
coord_plus = lambda x, y: (x[0] + y[0], x[1] + y[1])


def part1(grid: Grid) -> int:
    antinodes = set()
    nodes = defaultdict(set)
    for i_idx, i in enumerate(grid.rows):
        for j_idx, j in enumerate(i):
            if j != ".":
                nodes[j].add((i_idx, j_idx))

    for node, coords in nodes.items():
        for coord_pair in combinations(coords, 2):
            diff = coord_diff(coord_pair[0], coord_pair[1])
            antinode_1 = coord_plus(coord_pair[0], diff)
            antinode_2 = coord_diff(coord_pair[1], diff)
            if grid.in_grid(*antinode_1):
                antinodes.add(antinode_1)
            if grid.in_grid(*antinode_2):
                antinodes.add(antinode_2)
    return len(antinodes)


def part2(grid: Grid) -> int:
    antinodes = set()
    nodes = defaultdict(set)
    for i_idx, i in enumerate(grid.rows):
        for j_idx, j in enumerate(i):
            if j != ".":
                nodes[j].add((i_idx, j_idx))

    for node, coords in nodes.items():
        for coord_pair in combinations(coords, 2):
            in_grid = True
            i = 1
            diff = coord_diff(coord_pair[0], coord_pair[1])
            antinodes.add(coord_pair[0])
            antinodes.add(coord_pair[1])
            while in_grid:
                total_diff = (diff[0] * i, diff[1] * i)
                antinode = coord_plus(coord_pair[0], total_diff)
                if grid.in_grid(*antinode):
                    antinodes.add(antinode)
                    i += 1
                else:
                    in_grid = False
            in_grid = True
            i = 1
            while in_grid:
                total_diff = (diff[0] * i, diff[1] * i)
                antinode = coord_diff(coord_pair[0], total_diff)
                if grid.in_grid(*antinode):
                    antinodes.add(antinode)
                    i += 1
                else:
                    in_grid = False
    return len(antinodes)


if __name__ == "__main__":
    input_str = get_input()
    grid = Grid(input_str)
    GRID = [["." for _ in range(grid.width)] for _ in range(grid.height)]
    print(part1(grid))
    print(part2(grid))
