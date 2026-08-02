class Cell:
    def __init__(self, row: int, col: int, value: int = 0, locked: bool = False):
        self._row = row
        self._col = col
        self._value = value
        self._locked = locked

    @property
    def row(self) -> int:
        #row index (0-8)
        return self._row

    @property
    def col(self) -> int:
        #column index (0-8)
        return self._col

    @property
    def box(self) -> int:
        #3x3 box index (0-8)
        return (self._row // 3) * 3 + (self._col // 3)

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new_value: int) -> None:
        if self._locked:
            raise ValueError("cannot modify a locked cell")
        if not (0 <= new_value <= 9):
            raise ValueError("value must be between 0 and 9")
        self._value = new_value

    @property
    def locked(self) -> bool:
        return self._locked

    def is_empty(self) -> bool:
        return self._value == 0

    def is_filled(self) -> bool:
        return 1 <= self._value <= 9

    def __str__(self) -> str:
        return str(self._value) if self.is_filled() else "."

    def __repr__(self) -> str:
        return f"Cell(row={self._row}, col={self._col}, value={self._value}, locked={self._locked})"