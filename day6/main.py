from pathlib import Path
from enum import Enum, auto
from pprint import pp
import typing as t

FILE_DIR = Path(__file__).parent.absolute()
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


class Grid:
    def __init__(self, rows: list[str]):
        self.guard = (0, 0)
        self.rows = rows
        self.width = len(rows[0])
        self.height = len(rows)
        self.find_guard()
        self.direction = Directions.North
        self.guards_path = set()
        self.obstacles = []
        self.hit_record = set()

    def change_direction(self):
        match self.direction:
            case Directions.North:
                self.direction = Directions.East
            case Directions.East:
                self.direction = Directions.South
            case Directions.South:
                self.direction = Directions.West
            case Directions.West:
                self.direction = Directions.North

    def reset(self):
        self.hit_record = set()
        self.guard = self.original_guard
        self.direction = Directions.North

    def find_guard(self):
        for i_idx, i in enumerate(self.rows):
            for j_idx, j in enumerate(i):
                if j == "^":
                    self.guard = (i_idx, j_idx)
                    self.original_guard = (i_idx, j_idx)

    def parse_grid(self):
        for i_idx, i in enumerate(self.rows):
            for j_idx, j in enumerate(i):
                if j == "#":
                    self.obstacles.append((i_idx, j_idx))
                elif j == "^":
                    self.guard = (i_idx, j_idx)

    def populate_global_grid(self, row: int, column: int):
        global GRID
        GRID[row][column] = "X"

    def get_value(self, row: int, column: int) -> str:
        if row < 0 or column < 0:
            return "0"
        try:
            return self.rows[row][column]
        except IndexError:
            return "0"

    def get_value_using_direction(self, row: int, column: int, direction: Directions) -> tuple[str, int, int]:
        match direction:
            case Directions.North:
                return self.get_value(row - 1, column), row - 1, column
            case Directions.South:
                return self.get_value(row + 1, column), row + 1, column
            case Directions.East:
                return self.get_value(row, column + 1), row, column + 1
            case Directions.West:
                return self.get_value(row, column - 1), row, column - 1

    def move(self) -> bool:
        while True:
            self.populate_global_grid(*self.guard)
            val, i, j = self.get_value_using_direction(*self.guard, self.direction)
            if val == "0":
                return False
            elif val == "#":
                move_details = (i, j, self.direction)
                if move_details in self.hit_record:
                    return True
                self.hit_record.add(move_details)
                self.change_direction()
                continue
            self.guard = (i, j)
            self.guards_path.add(self.guard)


def part1(grid: Grid) -> int:
    grid.move()
    return sum([i.count("X") for i in GRID])


def part2(grid: Grid) -> int:
    grid.move()  # find path
    grid.reset()
    guard_path = grid.guards_path.copy()
    obs = []
    for i, j in guard_path:
        grid.reset()
        # add obstacle
        grid.rows[i] = grid.rows[i][:j] + "#" + grid.rows[i][j + 1 :]
        ret = grid.move()
        if ret:
            obs.append((i, j))
        # remove obstacle
        grid.rows[i] = grid.rows[i][:j] + "." + grid.rows[i][j + 1 :]
    return len(obs)


if __name__ == "__main__":
    input_str = get_input()
    grid = Grid(input_str)
    GRID = [["." for _ in range(grid.width)] for _ in range(grid.height)]
    print(part1(grid))
    print(part2(grid))
