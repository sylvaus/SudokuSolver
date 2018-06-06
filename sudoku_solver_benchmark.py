import csv
import glob
import time
import importlib
from typing import List, Optional

def load_sudoku(filename : str) -> List[Optional[int]]:
    with open(filename, newline='') as file:
        reader = csv.reader(file, delimiter=',')
        values = []
        for row in reader:
            values = row
            break
        return [None if value == '0' else int(value) for value in values]

def time_solver(sudoku_solver_class, sudokus, times=1000):
    start_time = time.clock()
    for sudoku in sudokus:
        for _ in range(times):
            sudoku_solver = sudoku_solver_class(sudoku)
            sudoku_solver.solve()

    return (time.clock() - start_time) / (times * len(sudokus))



if __name__ == '__main__':
    sudokus = list(map(load_sudoku, glob.glob("./sudokus/*.csv")))
    sudoku_solvers = glob.glob("sudoku_solvers/*.py")

    for sudoku_solver in sudoku_solvers:
        package = importlib.import_module(sudoku_solver.replace("/", ".").replace(".py", ""))
        average_time = time_solver(package.SudokuSolver, sudokus)
        print("Sudoku solver: {} has an average time of {}s".format(sudoku_solver.split("/")[-1], average_time))


