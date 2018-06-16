#!/usr/bin/env python3

import cv2
import numpy

from sudoku_img_helpers.detectors import detect_possible_sudokus
from sudoku_img_helpers.elements import Sudoku, Point


class SudokuExtractor:
    def __init__(self, image):
        self._image = cv2.resize(image, (900, 900))

    def extract_sudoku(self):
        image = cv2.resize(self._image, (900, 900))

        shapes = detect_possible_sudokus(image)
        sudoku_shapes = sorted(shapes, key=lambda shape: shape.area)

        for i, sudoku_shape in enumerate(reversed(sudoku_shapes)):
            # TODO: Implement something to check the next shape if nothing is found on the first one
            if i > 0:
                break

            # Rotate the sudoku
            # TODO: Handle case for angle oustide -90..90 range

            corners = Sudoku.sort_shape_corners(sudoku_shape)
            length = int(self._compute_average_length(corners))
            rotated_sudoku = Sudoku(Point(0, 0), Point(length, 0), Point(0, length), Point(length, length))
            rotated_corners = numpy.float32(list(map(lambda corner: corner.to_list(), rotated_sudoku.corners)))
            origin_corners = numpy.float32(list(map(lambda corner: corner.to_list(), corners)))

            transform = cv2.getPerspectiveTransform(origin_corners, rotated_corners)
            dst = cv2.warpPerspective(image, transform, (length, length))

    @staticmethod
    def _compute_average_length(corners):
        return (Point.distance(corners[0], corners[1]) +
                Point.distance(corners[0], corners[2]) +
                Point.distance(corners[2], corners[3]) +
                Point.distance(corners[1], corners[3])
                ) // 4
