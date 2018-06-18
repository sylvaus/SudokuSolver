#!/usr/bin/env python3
from typing import Any
from copy import deepcopy

import cv2
import numpy
import pytesseract as tess

from sudoku_img_helpers.detectors import detect_possible_sudokus
from sudoku_img_helpers.elements import Sudoku, Point


class SudokuExtractor:
    def __init__(self, image):
        self._image = deepcopy(image)
        self._sudoku_image = None
        self._sudoku_position = None

    def extract_sudoku(self):
        image = cv2.resize(self._image, (1200, 1200))

        shapes = detect_possible_sudokus(image)
        sudoku_shapes = sorted(shapes, key=lambda shape: shape.area)

        result = []
        for i, sudoku_shape in enumerate(reversed(sudoku_shapes)):
            # TODO: Implement something to check the next shape if nothing is found on the first one
            if i > 0:
                break

            self._sudoku_image, self._sudoku_position = self._rotate_and_crop_sudoku(image, sudoku_shape)
            ocr_image = self._prepare_image_for_ocr(self._sudoku_image)

            for cell in self._sudoku_position.cells:
                cell_image = cell.get_cell_image(ocr_image, 0.15)
                text = tess.image_to_string(cell_image,
                                            config="--psm 10 -c classify_bln_numeric_mode=1 --oem 1")

                result.append(self._text_to_int(text))

        return result

    @staticmethod
    def _prepare_image_for_ocr(sudoku_image):
        gray = cv2.cvtColor(sudoku_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (15, 15), 0)
        sudoku_image = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY, 11, 2)
        return sudoku_image

    @staticmethod
    def _text_to_int(val):
        if val in ["I", "l", "!"]:
            # TODO has to be improved
            # It should check the cell to see if there is a number or not
            return 1

        try:
            num = int(val)
        except ValueError:
            return None

        if 0 < num < 10:
            return num
        else:
            return None

    def _rotate_and_crop_sudoku(self, image, sudoku_shape) -> [Any, Sudoku]:
        # TODO: Handle case for angle oustide -90..90 range
        corners = Sudoku.sort_shape_corners(sudoku_shape)
        length = int(self._compute_average_length(corners))

        rotated_sudoku = Sudoku(Point(0, 0), Point(length, 0), Point(0, length), Point(length, length))

        rotated_corners = numpy.float32(list(map(lambda corner: corner.to_list(), rotated_sudoku.corners)))
        origin_corners = numpy.float32(list(map(lambda corner: corner.to_list(), corners)))

        transform = cv2.getPerspectiveTransform(origin_corners, rotated_corners)
        sudoku_image = cv2.warpPerspective(image, transform, (length, length))
        return sudoku_image, rotated_sudoku

    @staticmethod
    def _compute_average_length(corners):
        return (Point.distance(corners[0], corners[1]) +
                Point.distance(corners[0], corners[2]) +
                Point.distance(corners[2], corners[3]) +
                Point.distance(corners[1], corners[3])
                ) // 4

    def write_sudoku_values(self, values):
        image = deepcopy(self._sudoku_image)
        self._sudoku_position.write_in_cells(image, values)
        cv2.imshow("Sudoku", image)
        cv2.waitKey(0)

