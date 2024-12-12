from pathlib import Path
from enum import auto, Enum
from collections import defaultdict

FILE_DIR = Path(__file__).parent.absolute()


def get_input() -> list[str]:
    with open(FILE_DIR / "test_input.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


class Directions(Enum):
    North = auto()
    South = auto()
    East = auto()
    West = auto()


class Grid:
    def __init__(self, rows: list[str]):
        self.rows = rows
        self.width = len(rows[0])
        self.height = len(rows)
        self.all_directions = {Directions.North, Directions.East, Directions.South, Directions.West}
        self.coords_seen = set()
        self.regions: dict[str, list[set[tuple[int, int]]]] = defaultdict(list)

    def reset_grid(self):
        self.coords_seen = set()

    def get_value(self, row: int, column: int) -> str:
        if self.in_grid(row, column):
            return self.rows[row][column]
        return ""

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

    def find_region(self, row: int, column: int) -> set[tuple[int, int]]:
        val = self.get_value(row, column)
        region = set()
        coords = [(row, column)]
        last_direction = None
        while coords:
            current_coord = coords.pop()
            if current_coord in self.coords_seen:
                continue
            current_val = self.get_value(*current_coord)
            if val == current_val:
                region.add(current_coord)
                self.coords_seen.add(current_coord)
                for direction in self.all_directions:
                    next_val, *next_coord = self.get_value_using_direction(*current_coord, direction)
                    coords.append(tuple(next_coord))
        return region
    
    def get_perimeter(self, region_coords: set[tuple[int, int]]) -> int:
        # each coord has value 4 and loses one for each adj coord
        coord_vals = []
        for coord in region_coords:
            val = 4
            for direction in self.all_directions:
                next_val, *next_coord = self.get_value_using_direction(*coord, direction)
                if tuple(next_coord) in region_coords:
                    val -= 1
            coord_vals.append(val)
        return sum(coord_vals)
    
    def get_sides(self, region_coords: set[tuple[int, int]]) -> int:
        # Find continuous horizontal slices, if a boundary does match up with the bordering slice add 2 sides
        coord_vals = []
        for coord in region_coords:
            val = 4
            for direction in self.all_directions:
                next_val, *next_coord = self.get_value_using_direction(*coord, direction)
                if tuple(next_coord) in region_coords:
                    val -= 1
            coord_vals.append(val)
        return sum(coord_vals)
    
    def fence_cost(self, row: int, column: int) -> int:
        region = self.find_region(row, column)
        return len(region) * self.get_perimeter(region)
    
    def sides_cost(self, row: int, column:int) -> int:
        region = self.find_region(row, column)
        return len(region) * self.get_perimeter(region)


def part1(grid: Grid) -> int:
    prices = []
    for i_idx, i in enumerate(grid.rows):
        for j_idx, j in enumerate(i):
            prices.append(grid.fence_cost(i_idx, j_idx))
    return sum(prices)


def part2(grid: Grid) -> int:
    prices = []
    for i_idx, i in enumerate(grid.rows):
        for j_idx, j in enumerate(i):
            prices.append(grid.sides_cost(i_idx, j_idx))
    return sum(prices)


if __name__ == "__main__":
    input_str = get_input()
    grid = Grid(input_str)
    print(part1(grid))
    grid.reset_grid()
    print(part2(grid))
