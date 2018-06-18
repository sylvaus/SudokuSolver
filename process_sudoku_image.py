#!/usr/bin/env python3

import cv2

from sudoku_img_helpers.extractor import SudokuExtractor
from sudoku_solvers.metro_sudoku_solver import SudokuSolver

if __name__ == '__main__':
    image = cv2.imread("sudoku3.jpg")

    extractor = SudokuExtractor(image)
    values = extractor.extract_sudoku()
    solver = SudokuSolver(values)
    result = solver.solve()
    extractor.write_sudoku_values(result)


