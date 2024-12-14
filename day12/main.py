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

    def find_region(self, row: int, column: int) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
        val = self.get_value(row, column)
        region = set()
        coords = [(row, column, Directions.West)]
        edges = set()
        while coords:
            *current_coord, direction = coords.pop()
            current_coord = tuple(current_coord)
            current_val = self.get_value(*current_coord)
            if val == current_val:
                if current_coord in self.coords_seen:
                    continue
                region.add(current_coord)
                self.coords_seen.add(current_coord)
                for direction in self.all_directions:
                    next_val, *next_coord = self.get_value_using_direction(*current_coord, direction)
                    coords.append(tuple([*next_coord, direction]))
            else:
                edges.add((*current_coord, direction))
        return region, edges
    
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
    
    def fence_cost(self, row: int, column: int) -> int:
        region, edges = self.find_region(row, column)
        return len(region) * len(edges)
    
    def sides_cost(self, row: int, column:int) -> int:
        sides = 0
        direction_dict = defaultdict(list)
        region, edges = self.find_region(row, column)
        for row, column, direction in edges:
            direction_dict[direction].append((row, column))
        for direction in direction_dict:
            x = defaultdict(list)
            if direction in [Directions.East, Directions.West]:
                for row, column in direction_dict[direction]:
                    x[column].append(row)
            else:
                for row, column in direction_dict[direction]:
                    x[row].append(column)
            for lst in x.values():
                r = 1
                lst = sorted(lst)
                for i in range(len(lst)-1):
                    if lst[i]+1 != lst[i+1]:
                        r += 1
                sides += r
        return len(region) * sides


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
