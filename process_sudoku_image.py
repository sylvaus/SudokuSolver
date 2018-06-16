#!/usr/bin/env python3

import copy

import cv2
import numpy
import pytesseract as tess


from sudoku_img_helpers.elements import Point, Sudoku
from sudoku_img_helpers.extractor import SudokuExtractor
from sudoku_img_helpers.detectors import detect_possible_sudokus

if __name__ == '__main__':
    image = cv2.imread("sudoku3.jpg")
    image = cv2.resize(image, (900, 900))

    shapes = detect_possible_sudokus(image)

    sudoku_shapes = sorted(shapes, key=lambda shape: shape.area)

    for i, sudoku_shape in enumerate(reversed(sudoku_shapes)):
        if i > 0:
            break

        new_image = copy.deepcopy(image)
        sudoku = Sudoku.make_from_shape(sudoku_shape)
        sudoku.draw_cells(new_image)
        cell_image = sudoku._cells[4][4].get_cell_image(image)
        cv2.imshow("Cell{}".format(i), cell_image)
        print("Ok", tess.image_to_string(cell_image, config="--psm 10"))

        corners = Sudoku.sort_shape_corners(sudoku_shape)
        length = int(SudokuExtractor._compute_average_length(corners))
        rotated_sudoku = Sudoku(Point(0, 0), Point(length, 0), Point(0, length), Point(length, length))
        print(length)
        rotated_corners = numpy.float32(list(map(lambda corner: corner.to_list(), rotated_sudoku.corners)))
        origin_corners = numpy.float32(list(map(lambda corner: corner.to_list(), corners)))

        M = cv2.getPerspectiveTransform(origin_corners, rotated_corners)

        dst = cv2.warpPerspective(image, M, (length, length))

        cv2.imshow("ImageWarped{}".format(i), dst)
        mask = numpy.ones(image.shape[:2], dtype="uint8") * 0
        cv2.drawContours(mask, sudoku._cells[4][0].contour, 0, (255, 255, 255), -1)
        new_image = cv2.bitwise_and(new_image, new_image, mask=mask)
        cv2.drawContours(new_image, [sudoku_shape.approx], -1, (255, 255, 0), 2)
        # cv2.putText(new_image, sudoku_shape.shape_name, sudoku_shape.center, cv2.FONT_HERSHEY_SIMPLEX,
        #            0.5, (0, 0, 0), 2)

        cv2.imshow("Image{}".format(i), new_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
