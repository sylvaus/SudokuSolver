#!/usr/bin/env python3

from typing import Iterable
import cv2

from sudoku_img_helpers.shape import Shape


def detect_all_shapes(image) -> Iterable:
    # convert the image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imshow("blurred", blurred)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)
    # find contours in the thresholded image and initialize the
    # shape detector
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[1]
    return map(Shape, contours)


def is_shape_potential_sudoku(shape: Shape) -> bool:
    if shape is None:
        return False

    return shape.shape_name == Shape.RECTANGLE or shape.shape_name == Shape.SQUARE


def detect_possible_sudokus(image) -> Iterable:
    return filter(is_shape_potential_sudoku, detect_all_shapes(image))

