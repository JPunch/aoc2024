from pathlib import Path
from enum import Enum, auto
from pprint import pp
import typing as t

FILE_DIR = Path(__file__).parent.absolute()
TARGET_WORD = "XMAS"
MAS_LIST = ["M", "A", "S"]
GRID = []


def get_input() -> list[str]:
    with open(FILE_DIR / "input.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


class Directions(Enum):
    North = auto()
    South = auto()
    East = auto()
    West = auto()
    NorthEast = auto()
    NorthWest = auto()
    SouthEast = auto()
    SouthWest = auto()


class Grid:
    def __init__(self, rows: list[str]):
        self.rows = rows
        self.width = len(rows[0])
        self.height = len(rows)

    def populate_global_grid(self, row: int, column: int, direction: Directions):
        global GRID
        GRID[row][column] = self.get_value(row, column)
        for _ in range(3):
            val, row, column = self.get_value_using_direction(row, column, direction)
            GRID[row][column] = val

    def populate_global_grid_mas(
        self, row: int, column: int, direction: t.Literal[Directions.North, Directions.NorthWest]
    ):
        global GRID
        GRID[row][column] = self.get_value(row, column)
        if direction == Directions.North:
            # populate verical cross
            directions = [Directions.North, Directions.South, Directions.East, Directions.West]
        else:
            # populate diagonals
            directions = [Directions.NorthWest, Directions.SouthEast, Directions.NorthEast, Directions.SouthWest]
        for direction in directions:
            val, new_row, new_column = self.get_value_using_direction(row, column, direction)
            GRID[new_row][new_column] = val

    def get_value(self, row: int, column: int) -> str:
        if row < 0 or column < 0:
            return "0"
        try:
            return self.rows[row][column]
        except IndexError:
            return "0"

    def get_value_using_direction(self, row: int, column: int, direction: Directions) -> str:
        match direction:
            case Directions.North:
                return self.get_value(row - 1, column), row - 1, column
            case Directions.South:
                return self.get_value(row + 1, column), row + 1, column
            case Directions.East:
                return self.get_value(row, column + 1), row, column + 1
            case Directions.West:
                return self.get_value(row, column - 1), row, column - 1
            case Directions.NorthEast:
                return self.get_value(row - 1, column + 1), row - 1, column + 1
            case Directions.NorthWest:
                return self.get_value(row - 1, column - 1), row - 1, column - 1
            case Directions.SouthEast:
                return self.get_value(row + 1, column + 1), row + 1, column + 1
            case Directions.SouthWest:
                return self.get_value(row + 1, column - 1), row + 1, column - 1

    def search_direction(self, row: int, column: int, direction: Directions, word: str) -> bool:
        if word == "":
            return True
        val, new_row, new_column = self.get_value_using_direction(row, column, direction)
        if val == word[0]:
            return self.search_direction(new_row, new_column, direction, word[1:])

    def search_for_word(self, row: int, column: int, word: str = TARGET_WORD) -> int:
        total = 0
        if self.get_value(row, column) != TARGET_WORD[0]:
            return 0
        for direction in Directions:
            if self.search_direction(row, column, direction, TARGET_WORD[1:]):
                self.populate_global_grid(row, column, direction)
                total += 1
        return total

    def search_mas(self, row: int, column: int) -> int:
        if self.get_value(row, column) != "A":
            return 0
        # # check north south east west
        # north, *_ = self.get_value_using_direction(row, column, Directions.North)
        # south, *_ = self.get_value_using_direction(row, column, Directions.South)
        # east, *_ = self.get_value_using_direction(row, column, Directions.East)
        # west, *_ = self.get_value_using_direction(row, column, Directions.West)
        # ns = "A" + north + south
        # ew = "A" + east + west
        # # make sure all characters in each direction
        # if all([char in ns for char in MAS_LIST]+[char in ew for char in MAS_LIST]):
        #     self.populate_global_grid_mas(row, column, Directions.North)
        #     return 1
        # check diagonals
        northeast, *_ = self.get_value_using_direction(row, column, Directions.NorthEast)
        southwest, *_ = self.get_value_using_direction(row, column, Directions.SouthWest)
        northwest, *_ = self.get_value_using_direction(row, column, Directions.NorthWest)
        southeast, *_ = self.get_value_using_direction(row, column, Directions.SouthEast)
        nesw = "A" + northeast + southwest
        nwse = "A" + northwest + southeast
        # make sure all characters in each direction
        if all([char in nesw for char in MAS_LIST] + [char in nwse for char in MAS_LIST]):
            self.populate_global_grid_mas(row, column, Directions.NorthWest)
            return 1
        return 0


def part1(grid: Grid) -> int:
    total = 0
    for idx_r, row in enumerate(grid.rows):
        for idx_c, column in enumerate(row):
            if column == TARGET_WORD[0]:
                total += grid.search_for_word(idx_r, idx_c)
    return total


def part2(grid: Grid) -> int:
    total = 0
    for idx_r, row in enumerate(grid.rows):
        for idx_c, column in enumerate(row):
            if column == "A":
                total += grid.search_mas(idx_r, idx_c)
    return total


if __name__ == "__main__":
    input_str = get_input()
    grid = Grid(input_str)
    GRID = [["." for _ in range(grid.width)] for _ in range(grid.height)]
    print(part1(grid))
    GRID = [["." for _ in range(grid.width)] for _ in range(grid.height)]
    print(part2(grid))
