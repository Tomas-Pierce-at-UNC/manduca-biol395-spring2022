
import math


class Point:

    SQRT2 = math.sqrt(2)

    __slots__ = ("row", "column")

    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def distance(self, other):
        delta_row = self.row - other.row
        delta_col = self.column - other.column
        squares = (delta_row ** 2) + (delta_col ** 2)
        dist = math.sqrt(squares)
        return dist

    def eight_connected(self, other):
        return self.distance(other) == self.SQRT2

    def adjacents(self):
        return [
            Point(self.row - 1, self.column - 1),
            Point(self.row, self.column - 1),
            Point(self.row + 1, self.column - 1),
            Point(self.row - 1, self.column),
            Point(self.row + 1, self.column),
            Point(self.row - 1, self.column + 1),
            Point(self.row, self.column + 1),
            Point(self.row + 1, self.column + 1)
            ]
