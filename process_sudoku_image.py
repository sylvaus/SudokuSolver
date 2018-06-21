#!/usr/bin/env python3
import glob
import os

import cv2

from sudoku_img_helpers.elements import BOTTOM_LEFT
from sudoku_img_helpers.extractor import SudokuExtractor
from sudoku_solvers.metro_sudoku_solver import SudokuSolver
from sudoku_utils.csv import save_sudoku


def save(sudoku_values):
        index = 0
        filename = "sudokus/sudoku_{}.csv"
        while os.path.isfile(filename.format(index)):
            index += 1

        save_sudoku(filename.format(index), sudoku_values)


def should_save():
    retries = 3
    while retries > 0:
        answer = input("Save sudoku [y/n]: ")
        answer.lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        retries -= 0

    return False


def process_image(image):
    print("Processing Image")
    extractor = SudokuExtractor(image)
    found_values = extractor.extract_sudoku()
    print("Solving Sudoku")
    solver = SudokuSolver(found_values)
    result = solver.solve()
    solved_values = []
    for existing_value, found_value in zip(found_values, result):
        if existing_value is None:
            solved_values.append(found_value)
        else:
            solved_values.append(None)

    sudoku_solved = extractor.write_sudoku_values(solved_values, font_scale=3)
    sudoku_solved = extractor.write_sudoku_values(found_values, sudoku_solved,
                                                  color=(0, 0, 255), position=BOTTOM_LEFT, font_scale=1.5)
    cv2.imshow("Sudoku", sudoku_solved)
    cv2.waitKey(0)
    if should_save():
        print("Saving sudoku")
        save(found_values)
        print("Sudoku saved")


if __name__ == '__main__':
    filenames = glob.glob("./*.png") + glob.glob("./*.jpg")

    for filename in filenames:
        image = cv2.imread(filename)
        process_image(image)

