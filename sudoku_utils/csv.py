import csv
import os
from typing import List, Optional


def save_sudoku(filename, values):
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([value.get() for value in values])


def load_sudoku(filename : str) -> List[Optional[int]]:
    with open(filename, newline='') as file:
        reader = csv.reader(file, delimiter=',')
        values = []
        for row in reader:
            values = row
            break
        return [None if value == '0' else int(value) for value in values]