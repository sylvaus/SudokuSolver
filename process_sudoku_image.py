import copy
import cv2

from sudoku_img_helpers.elements import Point, Shape, Sudoku
from sudoku_img_helpers.detectors import detect_all_shapes, detect_possible_sudokus

if __name__ == '__main__':
    image = cv2.imread("sudoku.png")
    image = cv2.resize(image, (900, 900))

    shapes = detect_possible_sudokus(image)

    sudoku_shapes = sorted(shapes, key=lambda shape: shape.area)

    for i, sudoku_shape in enumerate(reversed(sudoku_shapes)):
        if i > 0:
            break

        new_image = copy.deepcopy(image)
        sudoku = Sudoku(sudoku_shape)
        sudoku.draw_corners(new_image)
        cv2.drawContours(new_image, [sudoku_shape.approx], -1, (255, 255, 0), 2)
        # cv2.putText(new_image, sudoku_shape.shape_name, sudoku_shape.center, cv2.FONT_HERSHEY_SIMPLEX,
        #            0.5, (0, 0, 0), 2)

        cv2.imshow("Image{}".format(i), new_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
