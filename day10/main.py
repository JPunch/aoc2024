from pathlib import Path
from enum import auto, Enum

FILE_DIR = Path(__file__).parent.absolute()


def get_input() -> list[str]:
    with open(FILE_DIR / "input.txt", "r") as f:
        lines = [list(map(int, line.strip())) for line in f.readlines()]
    return lines


class Directions(Enum):
    North = auto()
    South = auto()
    East = auto()
    West = auto()


class Grid:
    def __init__(self, rows: list[list[int]]):
        self.rows = rows
        self.width = len(rows[0])
        self.height = len(rows)
        self.all_driections = {Directions.North, Directions.East, Directions.South, Directions.West}

    def get_value(self, row: int, column: int) -> str:
        if row < 0 or column < 0:
            return "0"
        try:
            return self.rows[row][column]
        except IndexError:
            return "0"

    def get_value_using_direction(self, row: int, column: int, direction: Directions) -> tuple[int, int, int]:
        match direction:
            case Directions.North:
                return self.get_value(row - 1, column), row - 1, column
            case Directions.South:
                return self.get_value(row + 1, column), row + 1, column
            case Directions.East:
                return self.get_value(row, column + 1), row, column + 1
            case Directions.West:
                return self.get_value(row, column - 1), row, column - 1

    def in_grid(self, row: int, column: int) -> bool:
        return (0 <= row <= self.height - 1) and (0 <= column <= self.width - 1)

    def find_paths(self, row: int, column: int) -> int:
        path_starts = set()
        coords = [(row, column)]
        last_direction = None
        while coords:

            current_coord = coords.pop()
            current_val = self.get_value(*current_coord)
            for direction in self.all_driections:
                next_val, *next_coord = self.get_value_using_direction(*current_coord, direction)
                if next_val == current_val - 1:
                    if next_val != 0:
                        coords.append(next_coord)
                    else:
                        path_starts.add(tuple(next_coord))
        return len(path_starts)

    def find_paths_p2(self, row: int, column: int) -> int:
        total_paths = 0
        coords = [(row, column)]
        last_direction = None
        while coords:

            current_coord = coords.pop()
            current_val = self.get_value(*current_coord)
            for direction in self.all_driections:
                next_val, *next_coord = self.get_value_using_direction(*current_coord, direction)
                if next_val == current_val - 1:
                    if next_val != 0:
                        coords.append(next_coord)
                    else:
                        total_paths += 1
        return total_paths


def part1(grid: Grid) -> int:
    start_coords = set()
    for i_idx, i in enumerate(grid.rows):
        for j_idx, j in enumerate(i):
            if j == 9:
                start_coords.add((i_idx, j_idx))
    return sum([grid.find_paths(*coord) for coord in start_coords])


def part2(grid: Grid) -> int:
    start_coords = set()
    for i_idx, i in enumerate(grid.rows):
        for j_idx, j in enumerate(i):
            if j == 9:
                start_coords.add((i_idx, j_idx))
    return sum([grid.find_paths_p2(*coord) for coord in start_coords])


if __name__ == "__main__":
    input_str = get_input()
    grid = Grid(input_str)
    print(part1(grid))
    print(part2(grid))
