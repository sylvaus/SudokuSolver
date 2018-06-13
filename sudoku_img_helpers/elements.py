from typing import Optional, Tuple, List

import cv2


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

    def draw_on_image(self, image, marker_size: int = 10, thickness: int = 3, color: tuple = (0, 0, 255),
                      marker_type=cv2.MARKER_CROSS):
        cv2.drawMarker(image, (self._x, self._y), color,
                       markerType=marker_type, markerSize=marker_size, thickness=thickness)

    def to_list(self):
        return [self._x, self._y]


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

    def draw_on_image(self, image, thickness: int = 3, color: tuple = (0, 0, 255)):
        contours = [[self._top_left.to_list()], [self._top_right.to_list()],
                    [self._bottom_right.to_list()], [self._bottom_left.to_list()]]

        cv2.drawContours(image, [contours], -1, color, thickness)


class Shape:
    def __init__(self, center: Optional[Tuple] = None, contour: Optional[list] = None):
        self._shape = "unidentified"
        self._center = center
        self._contour = contour
        if contour is not None:
            self._area = cv2.contourArea(contour)
            self._perimeter = cv2.arcLength(contour, True)
            self._approx = cv2.approxPolyDP(contour, 0.04 * self._perimeter, True)
        else:
            self._area = None
            self._perimeter = None
            self._approx = None

    @property
    def shape_name(self):
        return self._shape

    @shape_name.setter
    def shape_name(self, value: str):
        self._shape = value

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, value: float):
        self._area = value

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = value

    @property
    def contour(self):
        return self._contour

    @contour.setter
    def contour(self, value):
        self._contour = value

    @property
    def approx(self):
        return self._approx

    @approx.setter
    def approx(self, value):
        self._approx = value


class Sudoku(Cell):
    def __init__(self, shape: Shape):
        self._shape = shape
        super().__init__(*self.sort_corners(shape.approx))
        self._corners = []
        self._cells = []
        bottom_corners = [self._bottom_left + (self._bottom_right - self._bottom_left) * (i / 9) for i in range(10)]
        top_corners = [self._top_left + (self._top_right - self._top_left) * (i / 9) for i in range(10)]

        for i in range(len(bottom_corners)):
            self._corners.append([
                bottom_corners[i] + (top_corners[i] - bottom_corners[i]) * (j / 9) for j in range(10)
            ])

        for row in range(9):
            for col in range(9):
                # TODO
                pass

    def draw_corners(self, image, *args, **kwargs):
        for lines in self._corners:
            for point in lines:
                point.draw_on_image(image, *args, **kwargs)

    @staticmethod
    def sort_corners(corners: list) -> List[Point]:
        """
        Sort quadrilateral corners as follows top_left, top_right, bottom_left, bottom_right
        :param corners:
        :return: Corners ordered as follows top_left, top_right, bottom_left, bottom_right
        """
        # conversion to list of tuples
        corners = list(map(lambda corner: Point(corner[0][0], corner[0][1]), corners))
        top_bottom_sorted = sorted(corners, key=lambda point: point.y)
        top_left, top_right = sorted(top_bottom_sorted[:2], key=lambda point: point.x)
        bottom_left, bottom_right = sorted(top_bottom_sorted[2:], key=lambda point: point.x)

        return [top_left, top_right, bottom_left, bottom_right]
