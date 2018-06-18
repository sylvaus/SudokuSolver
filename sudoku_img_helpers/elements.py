#!/usr/bin/env python3

from math import sqrt
from typing import Tuple, List

import cv2
import numpy

from sudoku_img_helpers.shape import Shape


class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self._x = int(x)
        self._y = int(y)

    def __add__(self, other: "Point") -> "Point":
        return Point(self._x + other.x, self._y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self._x - other.x, self._y - other.y)

    def __truediv__(self, divider: int) -> "Point":
        return Point(self._x // divider, self._y // divider)

    def __mul__(self, mult: float) -> "Point":
        return Point(int(self._x * mult), int(self._y * mult))

    def __str__(self):
        return "Point({},{})".format(self._x, self._y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = int(x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = int(y)

    @staticmethod
    def distance(start_point: "Point", end_point: "Point"):
        return sqrt((end_point.x - start_point.x) ** 2 +
                    (end_point.y - start_point.y) ** 2)

    def draw_on_image(self, image, marker_size: int = 10, thickness: int = 3, color: tuple = (0, 0, 255),
                      marker_type=cv2.MARKER_CROSS):
        cv2.drawMarker(image, (self._x, self._y), color,
                       markerType=marker_type, markerSize=marker_size, thickness=thickness)

    def to_list(self) -> List:
        return [self._x, self._y]

    def to_tuple(self) -> Tuple:
        return self._x, self._y


class Cell:
    def __init__(self, top_left: Point, top_right: Point, bottom_left: Point, bottom_right: Point):
        self._top_left = top_left
        self._top_right = top_right
        self._bottom_left = bottom_left
        self._bottom_right = bottom_right

    @property
    def top_left(self):
        return self._top_left

    @top_left.setter
    def top_left(self, point: Point):
        self._top_left = point

    @property
    def top_right(self):
        return self._top_right

    @top_right.setter
    def top_right(self, point: Point):
        self._top_right = point

    @property
    def bottom_left(self):
        return self._bottom_left

    @bottom_left.setter
    def bottom_left(self, point: Point):
        self._bottom_left = point

    @property
    def bottom_right(self):
        return self._bottom_right

    @bottom_right.setter
    def bottom_right(self, point: Point):
        self._bottom_right = point

    @property
    def contour(self):
        return numpy.array([[self._top_left.to_list()], [self._top_right.to_list()],
                            [self._bottom_right.to_list()], [self._bottom_left.to_list()]], dtype=numpy.int32)

    @property
    def center(self):
        return (self._top_left + self._top_right + self._bottom_left + self._bottom_right) / 4

    @property
    def corners(self):
        return [self._top_left, self._top_right, self._bottom_left, self._bottom_right]

    def draw_on_image(self, image, thickness: int = 3, color: tuple = (0, 0, 255)):
        cv2.drawContours(image, [self.contour], -1, color, thickness)

    def write_on_image(self, image, text: str, font=cv2.FONT_HERSHEY_PLAIN, font_scale=2, color=(0, 0, 0), thickness=4):
        size, baseline = cv2.getTextSize(text, font, font_scale, thickness=thickness)
        cv2.putText(image, text, (self.center + Point(-size[0]/2, size[1]/2)).to_tuple(),
                    font, font_scale, color, thickness=thickness)

    def get_cell_image(self, image, offset: float=0):
        x_max, x_min, y_max, y_min = self.get_bounds()

        center = Point((x_max + x_min) // 2, (y_max + y_min) // 2)
        top_corner = Point(x_min, y_min)
        sub_image = cv2.getRectSubPix(image, (x_max - x_min, y_max - y_min), center.to_tuple())

        mask = numpy.ones(sub_image.shape, dtype="uint8") * 255
        top_left = self._top_left - top_corner
        top_right = self._top_right - top_corner
        bottom_right = self._bottom_right - top_corner
        bottom_left = self._bottom_left - top_corner

        if abs(offset) > 0.0001:
            down_diag = (self._bottom_right - self._top_left) * offset
            up_diag = (self.top_right - self.bottom_left) * offset
            top_left += down_diag
            top_right -= up_diag
            bottom_left += up_diag
            bottom_right -= down_diag

        contour = [numpy.array([[top_left.to_list()], [top_right.to_list()],
                                [bottom_right.to_list()], [bottom_left.to_list()]], dtype=numpy.int32)]
        cv2.drawContours(mask, contour, 0, (0, 0, 0), -1)
        return cv2.bitwise_or(sub_image, mask)

    def get_bounds(self):
        x_positions = [self._top_left.x, self._top_right.x, self._bottom_left.x, self._bottom_right.x]
        y_positions = [self._top_left.y, self._top_right.y, self._bottom_left.y, self._bottom_right.y]
        x_max = max(x_positions)
        x_min = min(x_positions)
        y_max = max(y_positions)
        y_min = min(y_positions)
        return x_max, x_min, y_max, y_min


class Sudoku(Cell):
    def __init__(self, top_left: Point, top_right: Point, bottom_left: Point, bottom_right: Point):
        super().__init__(top_left, top_right, bottom_left, bottom_right)
        self._corners = []
        self._cells = []
        left_corners = [self._top_left + (self._bottom_left - self._top_left) * (i / 9) for i in range(10)]
        right_corners = [self._top_right + (self._bottom_right - self._top_right) * (i / 9) for i in range(10)]

        for i in range(len(left_corners)):
            self._corners.append([
                left_corners[i] + (right_corners[i] - left_corners[i]) * (j / 9) for j in range(10)
            ])

        for row in range(9):
            for col in range(9):
                self._cells.append(Cell(self._corners[row][col], self._corners[row][col + 1],
                                        self._corners[row + 1][col], self._corners[row + 1][col + 1]))

    @property
    def cells(self) -> List[Cell]:
        return self._cells

    def draw_corners(self, image, *args, **kwargs) -> None:
        for rows in self._corners:
            for point in rows:
                point.draw_on_image(image, *args, **kwargs)

    def draw_cells(self, image, *args, **kwargs) -> None:
        for cell in self._cells:
            cell.draw_on_image(image, *args, **kwargs)

    def write_in_cells(self, image, values, font=cv2.FONT_HERSHEY_PLAIN, font_scale=2, color=(0, 0, 0)):
        assert len(self._cells) == len(values)

        for cell, value in zip(self._cells, values):
            if value is None:
                continue
            cell.write_on_image(image, str(value), font, font_scale, color)

    @staticmethod
    def sort_shape_corners(shape: Shape) -> List[Point]:
        """
        Sort shape four corners contained in approx as follows top_left, top_right, bottom_left, bottom_right
        :param shape:
        :return: Corners ordered as follows top_left, top_right, bottom_left, bottom_right
        """
        # Ensures there are four corners in approx
        assert shape.shape_name == Shape.RECTANGLE or shape.shape_name == shape.SQUARE

        # conversion to list of tuples
        corners = list(map(lambda corner: Point(corner[0][0], corner[0][1]), shape.approx))
        top_bottom_sorted = sorted(corners, key=lambda point: point.y)
        top_left, top_right = sorted(top_bottom_sorted[:2], key=lambda point: point.x)
        bottom_left, bottom_right = sorted(top_bottom_sorted[2:], key=lambda point: point.x)

        return [top_left, top_right, bottom_left, bottom_right]

    @staticmethod
    def make_from_shape(shape: Shape) -> "Sudoku":
        return Sudoku(*Sudoku.sort_shape_corners(shape))
