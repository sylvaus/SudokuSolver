#!/usr/bin/env python3

import cv2


class Shape:
    UNIDENTIFIED = "unidentified"
    TRIANGLE = "triangle"
    SQUARE = "square"
    RECTANGLE = "rectangle"
    PENTAGON = "pentagon"
    CIRCLE = "circle"

    def __init__(self, contour):
        self._shape = self.UNIDENTIFIED

        m = cv2.moments(contour)
        if m["m00"] < 0.1:
            # Nothing to be found
            return

        self._center = (int((m["m10"] / m["m00"])), int((m["m01"] / m["m00"])))
        self._contour = contour
        self._area = cv2.contourArea(contour)
        self._perimeter = cv2.arcLength(contour, True)
        self._approx = cv2.approxPolyDP(contour, 0.04 * self._perimeter, True)
        self._shape = self.find_shape_name(self._approx)

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

    @staticmethod
    def find_shape_name(approx):
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            return Shape.TRIANGLE

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            if 0.95 <= ar <= 1.05:
                return Shape.SQUARE
            else:
                return Shape.RECTANGLE

        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            return Shape.PENTAGON

        # otherwise, we assume the shape is a circle
        else:
            return Shape.CIRCLE
