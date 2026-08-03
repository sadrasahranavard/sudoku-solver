import pytest
from src.models.board import Board
from src.solver.validator import is_board_valid

def test_create_empty_board():
    board = Board()
    assert len(board.get_empty_positions()) == 81
    assert not board.is_full()

def test_create_board_from_grid():
    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    board = Board(grid)
    assert board.get_value(0, 0) == 5
    assert board.get_value(0, 1) == 3
    assert board.get_value(0, 2) == 0
    assert board.is_locked(0, 0)  # Non-zero = given
    assert not board.is_locked(0, 2)  # Zero = not given

def test_invalid_grid_raises_error():
    #wrong rows
    with pytest.raises(ValueError):
        Board([[1, 2, 3, 4, 5, 6, 7, 8, 9]])  #1 row

    #wrong columns
    with pytest.raises(ValueError):
        Board([[1, 2] for _ in range(9)])  #9 rows 2 columns each

def test_get_set_value():
    board = Board()
    board.set_value(0, 0, 5)
    assert board.get_value(0, 0) == 5
    assert not board.is_empty(0, 0)

def test_cannot_modify_locked_cell():
    grid = [[5 if r == 0 and c == 0 else 0 for c in range(9)] for r in range(9)]
    board = Board(grid)

    with pytest.raises(ValueError, match="cannot modify a locked cell"):
        board.set_value(0, 0, 9)

def test_get_row():
    board = Board()
    board.set_value(0, 0, 5)
    board.set_value(0, 1, 3)

    row = board.get_row(0)
    assert row[0] == 5
    assert row[1] == 3
    assert len(row) == 9

def test_get_col():
    board = Board()
    board.set_value(0, 0, 5)
    board.set_value(1, 0, 3)

    col = board.get_col(0)
    assert col[0] == 5
    assert col[1] == 3
    assert len(col) == 9

def test_get_box():
    board = Board()
    board.set_value(0, 0, 5)
    board.set_value(1, 1, 3)

    box = board.get_box(0, 0)
    assert 5 in box
    assert 3 in box
    assert len(box) == 9

def test_get_row_cells():
    board = Board()
    cells = board.get_row_cells(0)
    assert len(cells) == 9
    assert cells[0].row == 0
    assert cells[0].col == 0

def test_get_col_cells():
    board = Board()
    cells = board.get_col_cells(0)
    assert len(cells) == 9
    assert cells[1].row == 1
    assert cells[1].col == 0

def test_get_box_cells():
    board = Board()
    cells = board.get_box_cells(0, 0)
    assert len(cells) == 9

def test_copy_is_independent():
    board = Board()
    board.set_value(0, 0, 5)
    board.set_value(0, 1, 3)

    copy_board = board.copy()
    assert copy_board.get_value(0, 0) == 5
    assert copy_board.get_value(0, 1) == 3

    #modify empty cells
    copy_board.set_value(1, 1, 9)
    assert board.is_empty(1, 1)  #original
    assert copy_board.get_value(1, 1) == 9

def test_from_string():
    board_str = """
    5 3 . . 7 . . . .
    6 . . 1 9 5 . . .
    . 9 8 . . . . 6 .
    8 . . . 6 . . . 3
    4 . . 8 . 3 . . 1
    7 . . . 2 . . . 6
    . 6 . . . . 2 8 .
    . . . 4 1 9 . . 5
    . . . . 8 . . 7 9
    """
    board = Board.from_string(board_str)
    assert board.get_value(0, 0) == 5
    assert board.get_value(0, 2) == 0
    assert board.get_value(1, 0) == 6

def test_is_full():
    board = Board()
    assert not board.is_full()

    for r in range(9):
        for c in range(9):
            board.set_value(r, c, 1)

    assert board.is_full()

def test_empty_positions():
    board = Board()
    board.set_value(0, 0, 5)
    empty = board.get_empty_positions()
    assert len(empty) == 80
    assert (0, 0) not in empty

def test_to_grid():
    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    board = Board(grid)
    assert board.to_grid() == grid

def test_str_representation():
    board = Board()
    board.set_value(0, 0, 5)
    output = str(board)
    assert "5" in output
    assert "+-------+-------+-------+" in output