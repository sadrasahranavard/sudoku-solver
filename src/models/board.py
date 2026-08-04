from typing import List, Tuple, Optional
from src.models.cell import Cell


class Board:
    SIZE = 9
    BOX_SIZE = 3

    def __init__(self, grid: Optional[List[List[int]]] = None):
        self._cells = []
        if grid:
            self._initialize_from_grid(grid)
        else:
            self._initialize_empty()

    def _initialize_empty(self) -> None:
        self._cells = [
            [Cell(row, col, 0, False) for col in range(self.SIZE)]
            for row in range(self.SIZE)
        ]

    def _initialize_from_grid(self, grid: List[List[int]]) -> None:
        if len(grid) != self.SIZE:
            raise ValueError(f"Grid must have {self.SIZE} rows")

        self._cells = []
        for row in range(self.SIZE):
            if len(grid[row]) != self.SIZE:
                raise ValueError(f"Row {row} must have {self.SIZE} columns")

            row_cells = []
            for col in range(self.SIZE):
                value = grid[row][col]
                if not (0 <= value <= 9):
                    raise ValueError(f"Invalid value at ({row}, {col}): {value}")
                row_cells.append(Cell(row, col, value, value != 0))
            self._cells.append(row_cells)

    def get_cell(self, row: int, col: int) -> Cell:
        self._validate_position(row, col)
        return self._cells[row][col]

    def get_value(self, row: int, col: int) -> int:
        return self.get_cell(row, col).value

    def set_value(self, row: int, col: int, value: int) -> None:
        self.get_cell(row, col).value = value

    def is_empty(self, row: int, col: int) -> bool:
        return self.get_cell(row, col).is_empty()

    def is_locked(self, row: int, col: int) -> bool:
        return self.get_cell(row, col).locked

    def get_row(self, row: int) -> List[int]:
        self._validate_row(row)
        return [cell.value for cell in self._cells[row]]

    def get_col(self, col: int) -> List[int]:
        self._validate_col(col)
        return [self._cells[row][col].value for row in range(self.SIZE)]

    def get_box(self, row: int, col: int) -> List[int]:
        self._validate_position(row, col)
        start_row = (row // self.BOX_SIZE) * self.BOX_SIZE
        start_col = (col // self.BOX_SIZE) * self.BOX_SIZE
        values = []
        for r in range(start_row, start_row + self.BOX_SIZE):
            for c in range(start_col, start_col + self.BOX_SIZE):
                values.append(self._cells[r][c].value)
        return values

    def get_row_cells(self, row: int) -> List[Cell]:
        self._validate_row(row)
        return self._cells[row][:]

    def get_col_cells(self, col: int) -> List[Cell]:
        self._validate_col(col)
        return [self._cells[r][col] for r in range(self.SIZE)]

    def get_box_cells(self, row: int, col: int) -> List[Cell]:
        self._validate_position(row, col)
        start_row = (row // self.BOX_SIZE) * self.BOX_SIZE
        start_col = (col // self.BOX_SIZE) * self.BOX_SIZE
        cells = []
        for r in range(start_row, start_row + self.BOX_SIZE):
            for c in range(start_col, start_col + self.BOX_SIZE):
                cells.append(self._cells[r][c])
        return cells

    def get_empty_positions(self) -> List[Tuple[int, int]]:
        positions = []
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self._cells[row][col].is_empty():
                    positions.append((row, col))
        return positions

    def is_full(self) -> bool:
        return len(self.get_empty_positions()) == 0

    def copy(self) -> 'Board':
        grid = self.to_grid()
        new_board = Board(grid)
    
        for r in range(9):
            for c in range(9):
                new_board._cells[r][c]._locked = self._cells[r][c].locked
        return new_board

    def to_grid(self) -> List[List[int]]:
        return [[cell.value for cell in row] for row in self._cells]

    @staticmethod
    def from_string(board_str: str) -> 'Board':
        lines = [
            line.strip()
            for line in board_str.strip().split('\n')
            if line.strip()
        ]

        grid = []
        for line in lines:
            row = []
            for char in line.split():
                if char in ('.', '0'):
                    row.append(0)
                elif char.isdigit():
                    row.append(int(char))
                else:
                    raise ValueError(f"invalid character in puzzle: '{char}'")
            if len(row) == Board.SIZE:
                grid.append(row)

        if len(grid) != Board.SIZE:
            raise ValueError(f"board must have {Board.SIZE} rows, got {len(grid)}")

        return Board(grid)

    def __str__(self) -> str:
        result = []
        result.append("+-------+-------+-------+")
        for i in range(self.SIZE):
            row_str = "| "
            for j in range(self.SIZE):
                cell = self._cells[i][j]
                row_str += str(cell) + (" | " if j % 3 == 2 else " ")
            result.append(row_str)
            if i % 3 == 2:
                result.append("+-------+-------+-------+")
        return "\n".join(result)

    def __repr__(self) -> str:
        filled = sum(1 for row in self._cells for cell in row if cell.is_filled())
        return f"board({filled}/81 cells filled)"

    def _validate_row(self, row: int) -> None:
        """Validate row index."""
        if not (0 <= row < self.SIZE):
            raise ValueError(f"row must be between 0 and {self.SIZE - 1}")

    def _validate_col(self, col: int) -> None:
        """Validate column index."""
        if not (0 <= col < self.SIZE):
            raise ValueError(f"column must be between 0 and {self.SIZE - 1}")

    def _validate_position(self, row: int, col: int) -> None:
        self._validate_row(row)
        self._validate_col(col)