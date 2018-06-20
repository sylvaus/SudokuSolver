from sudoku_utils.csv import load_sudoku

SUDOKU_STR = """
=======================================
|| {} | {} | {} || {} | {} | {} || {} | {} | {} ||
---------------------------------------
|| {} | {} | {} || {} | {} | {} || {} | {} | {} ||
---------------------------------------
|| {} | {} | {} || {} | {} | {} || {} | {} | {} ||
=======================================
|| {} | {} | {} || {} | {} | {} || {} | {} | {} ||
---------------------------------------
|| {} | {} | {} || {} | {} | {} || {} | {} | {} ||
---------------------------------------
|| {} | {} | {} || {} | {} | {} || {} | {} | {} ||
=======================================
|| {} | {} | {} || {} | {} | {} || {} | {} | {} ||
---------------------------------------
|| {} | {} | {} || {} | {} | {} || {} | {} | {} ||
---------------------------------------
|| {} | {} | {} || {} | {} | {} || {} | {} | {} ||
=======================================
"""


class Cell:
    def __init__(self, row, col, square):
        row.add_cell(self)
        col.add_cell(self)
        square.add_cell(self)
        self._row = row
        self._col = col
        self._square = square
        self.value = None
        self._possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self._weight_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._tried_values = []
        self._linked_cells = []

    def __str__(self):
        return str(self.value)

    def compute_next_linked_cells(self):
        self_index = self._row.cells.index(self)
        self._linked_cells = self._row.cells[self_index + 1:]

        self_index = self._col.cells.index(self)
        for cell in self._col.cells[self_index + 1:]:
            if self._linked_cells.count(cell) == 0:
                self._linked_cells.append(cell)

        self_index = self._square.cells.index(self)
        for cell in self._square.cells[self_index + 1:]:
            if self._linked_cells.count(cell) == 0:
                self._linked_cells.append(cell)

    def compute_all_linked_cells(self):
        self._linked_cells = self._row.cells[:]

        for cell in self._col.cells:
            if self._linked_cells.count(cell) == 0:
                self._linked_cells.append(cell)

        for cell in self._square.cells:
            if self._linked_cells.count(cell) == 0:
                self._linked_cells.append(cell)

    def increase_weight(self, value):
        if self.value is not None:
            return True
        self._weight_values[value] += 1

        if self._weight_values[value] == 1:
            self._possible_values.remove(value)

        if len(self._possible_values) == 0:
            return False
        return True

    def decrease_weight(self, value):
        if self.value is not None:
            return
        self._weight_values[value] -= 1
        if self._weight_values[value] == 0:
            self._possible_values.append(value)

    def set_next_possible(self):
        while len(self._possible_values) > 0:
            if self.value is not None:
                self.decrease_weight_others(self.value)

            self.value = self._possible_values.pop()
            self._tried_values.append(self.value)
            if self.increase_weight_others(self.value):
                return True

        return False

    def increase_weight_others(self, value):
        result = True
        for cell in self._linked_cells:
            if not cell.increase_weight(value):
                result = result and False
        return result

    def decrease_weight_others(self, value):
        for cell in self._linked_cells:
            cell.decrease_weight(value)

    def reset(self):
        self.decrease_weight_others(self.value)
        self._possible_values += self._tried_values
        self._tried_values = []
        self.value = None


class CellGroup:
    def __init__(self):
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)


class SudokuSolver:
    def __init__(self, values):
        assert len(values) == 81, "The values are expected in one array"

        self._rows = [CellGroup() for _ in range(9)]
        self._cols = [CellGroup() for _ in range(9)]
        self._squares = [CellGroup() for _ in range(9)]

        self._cells = []
        for row_index in range(9):
            for col_index in range(9):
                row = self._rows[row_index]
                col = self._cols[col_index]
                square = self._squares[col_index // 3 + (row_index // 3) * 3]
                self._cells.append(Cell(row, col, square))

        self._modifiable_cells = []
        for index, value in enumerate(values):
            if value is None:
                self._modifiable_cells.append(self._cells[index])
                self._cells[index].compute_next_linked_cells()
            else:
                self._cells[index].value = value
                self._cells[index].compute_all_linked_cells()

        for index, value in enumerate(values):
            if value is not None:
                self._cells[index].increase_weight_others(value)

    def solve(self):
        index = 0
        target = len(self._modifiable_cells)
        while index < target:
            cell = self._modifiable_cells[index]

            if cell.set_next_possible():
                index += 1
                continue
            else:
                cell.reset()
                index -= 1
                if index < 0:
                    break

        if index == target:
            return [cell.value for cell in self._cells]
        else:
            print("No solution could be found")

    def print_sudoku(self):
        print(SUDOKU_STR.format(*self._cells))


if __name__ == '__main__':
    values = load_sudoku("../sudokus/sudoku_0.csv")
    sudoku_solver = SudokuSolver(values)
    sudoku_solver.print_sudoku()
    sudoku_solver.solve()
    sudoku_solver.print_sudoku()
