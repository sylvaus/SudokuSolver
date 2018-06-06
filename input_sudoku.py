import csv
import os
from tkinter import Tk, Spinbox, Button, mainloop, Frame, LEFT, TOP


class InputSudoku(Frame):
    def __init__(self, master):
        super(InputSudoku, self).__init__(master)
        self.pack()

        self._values = []
        self._frames = [Frame(self) for _ in range(9)]
        for frame in self._frames:
            for _ in range(9):
                spin_box = Spinbox(frame, from_=0, to=10, width=2)
                spin_box.pack(side=LEFT)
                self._values.append(spin_box)

            frame.pack(side=TOP)

        self.button_save = Button(self, text="Save", command=self.save)
        self.button_save.pack(side=TOP)

    def start(self):
        mainloop()

    def save(self):
        index = 0
        filename = "sudokus/sudoku_{}.csv"
        while os.path.isfile(filename.format(index)):
            index += 1

        with open(filename.format(index), 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([value.get() for value in self._values])


if __name__ == '__main__':
    input_sudoku = InputSudoku(Tk())
    input_sudoku.start()
