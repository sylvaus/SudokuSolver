from typing import Iterable
import cv2

from sudoku_img_helpers.elements import Shape

def detect_shape(contour):
    m = cv2.moments(contour)
    if m["m00"] < 0.1:
        return None
    cX = int((m["m10"] / m["m00"]))
    cY = int((m["m01"] / m["m00"]))

    shape = Shape((cX, cY), contour)

    # if the shape is a triangle, it will have 3 vertices
    if len(shape.approx) == 3:
        shape.shape_name = "triangle"

    # if the shape has 4 vertices, it is either a square or
    # a rectangle
    elif len(shape.approx) == 4:
        # compute the bounding box of the contour and use the
        # bounding box to compute the aspect ratio
        (x, y, w, h) = cv2.boundingRect(shape.approx)
        ar = w / float(h)

        # a square will have an aspect ratio that is approximately
        # equal to one, otherwise, the shape is a rectangle
        if 0.95 <= ar <= 1.05:
            shape.shape_name = "square"
        else:
            shape.shape_name = "rectangle"

    # if the shape is a pentagon, it will have 5 vertices
    elif len(shape.approx) == 5:
        shape.shape_name = "pentagon"

    # otherwise, we assume the shape is a circle
    else:
        shape.shape_name = "circle"

    # return the name of the shape
    return shape


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
    return map(detect_shape, contours)


def is_shape_potential_sudoku(shape: Shape) -> bool:
    if shape is None:
        return False

    return shape.shape_name == "rectangle" or shape.shape_name == "square"


def detect_possible_sudokus(image) -> Iterable:
    return filter(is_shape_potential_sudoku, detect_all_shapes(image))

