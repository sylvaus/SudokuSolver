import copy
import cv2


class Shape:
    def __init__(self):
        self._shape = "unidentified"
        self._area = 0
        self._center = (0, 0)
        self._contour = None

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


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        m = cv2.moments(c)
        if m["m00"] < 0.1:
            return None
        cX = int((m["m10"] / m["m00"]))
        cY = int((m["m01"] / m["m00"]))

        shape = Shape()
        shape.center = (cX, cY)
        shape.area = cv2.contourArea(c)
        shape.contour = c

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape.shape_name = "triangle"

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
                shape.shape_name = "square"
            else:
                shape.shape_name = "rectangle"

        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape.shape_name = "pentagon"

        # otherwise, we assume the shape is a circle
        else:
            shape.shape_name = "circle"

        # return the name of the shape
        return shape


def is_shape_potential_sudoku(shape: Shape) -> bool:
    if shape is None:
        return False

    return shape.shape_name == "rectangle" or shape.shape_name == "square"


if __name__ == '__main__':
    image = cv2.imread("sudoku.png")
    image = cv2.resize(image, (900, 900))

    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imshow("blurred", blurred)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[1]

    sd = ShapeDetector()
    cv2.imshow("threshold", thresh)
    shapes = filter(is_shape_potential_sudoku, map(sd.detect, cnts))

    sudokus = sorted(shapes, key=lambda shape: shape.area)

    for i, sudoku in enumerate(reversed(sudokus)):
        if i > 3:
            break

        new_image = copy.deepcopy(image)
        cv2.drawContours(new_image, [sudoku.contour], -1, (255, 255, 0), 2)
        cv2.putText(new_image, sudoku.shape_name, sudoku.center, cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 2)

        cv2.imshow("Image{}".format(i), new_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
