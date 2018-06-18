#!/usr/bin/env python3

import copy

import cv2
import numpy
import pytesseract as tess


from sudoku_img_helpers.elements import Point, Sudoku
from sudoku_img_helpers.extractor import SudokuExtractor
from sudoku_img_helpers.detectors import detect_possible_sudokus

if __name__ == '__main__':
    image = cv2.imread("sudoku4.jpg")

    extractor = SudokuExtractor(image)
    print(extractor.extract_sudoku())

