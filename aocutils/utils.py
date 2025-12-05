from dataclasses import dataclass
from typing import Generic, TypeVar
import os


def loader(filepath):
    with open(filepath, 'r') as file:
        return file.read().splitlines()

T = TypeVar('T')

@dataclass()
class Grid:
    total_columns: int
    total_rows: int

    cells: list[list[T]]
    cell_type: Generic[T]

    def __init__(self, input_string: list[str], target_type: type, column_split:str = ""):
        self.total_rows = len(input_string)
        self.total_columns = len(input_string[0])

        self.cells = []
        self.cell_type = target_type

        for line in input_string:
            if column_split:
                self.cells.append(line.split(column_split))
            else:
                self.cells.append([col for col in line])

        self.convert_cells()

    def convert_cells(self):
        """
        Converts all cells in Grid to Type T
        :return:
        """
        for i, row in enumerate(self.cells):
            for j, value in enumerate(row):
                try:
                    if self.cell_type is float and isinstance(value, str):
                        self.cells[i][j] = float(value)
                    elif self.cell_type is int and isinstance(value, str):
                        self.cells[i][j] = int(float(value))
                    elif self.cell_type is str:
                        self.cells[i][j] = str(value)
                    else:
                        raise ValueError(f"Unsupported target type: {self.cell_type}")
                except ValueError as e:
                    raise ValueError(f"Error converting value {value!r} at position ({i}, {j}): {e}")

    def __str__(self):
        return "\n".join(["".join([str(cell) for cell in row]) for row in self.cells])

    def row(self, row):
        if row >= self.total_rows:
            raise IndexError(f"{row} greater than Grid's height ({self.total_rows})")
        return self.cells[row]

    def rows_yield(self):
        for i in range(self.total_rows):
            yield self.row(i)

    def column(self, column):
        if column >= self.total_columns:
            raise IndexError(f"{column} greater than Grid's height ({self.total_columns})")
        return [row[column] for row in self.cells]

    def columns_yield(self):
        for i in range(self.total_columns):
            yield self.column(i)

    def cell(self, row, column):
        if row >= self.total_rows:
            raise IndexError(f"{row} greater than Grid's height ({self.total_rows})")
        if column >= self.total_columns:
            raise IndexError(f"{column} greater than Grid's height ({self.total_columns})")
        return self.cells[row][column]

    def is_cell_edge(self, row, column):
        return (row == 0 or row == self.total_rows) \
            and (column == 0 or column == self.total_columns)

    def is_cell_valid(self, row, column):
        return 0 <= row <= self.total_rows \
            and 0 <= column <= self.total_columns

    def get_neighbours(self, central_row, central_column, include_diagonals: bool = False):
        #                  Left       Up     Right   Down
        moves_to_check = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        if include_diagonals:
            #                       TopLeft TopRight  BtmLeft  BtmRight
            moves_to_check.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])

        coordinates_to_check = [(row + central_row, column + central_column) for row, column in moves_to_check]
        for row, column in coordinates_to_check:
            # Continue if Out of Bounds
            if not self.is_cell_valid(row, column):
                continue
            yield self.cell(row, column), (row, column)

    def find_value(self, value: T) -> list[tuple[int, int]]:
        """

        :param value: Value to find
        :return: List of Coordinates where value was found
        """
        results = []
        for x, row in enumerate(self.rows_yield()):
            for y, column in enumerate(row):
                if column == value:
                    results.append((x, y))
        return results

def manhattan_distance(source_xy: tuple[int,int], target_xy: tuple[int,int]):
    dist_x = abs(source_xy[0] - target_xy[0])
    dist_y = abs(source_xy[1] - target_xy[1])
    return dist_x + dist_y
