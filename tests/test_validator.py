import pytest
from src.models.board import Board
from src.solver.validator import is_valid_move, get_possible_values, is_board_valid, is_solved

def test_is_valid_move_empty_board():
    board = Board()
    assert is_valid_move(board, 0, 0, 5)
    assert is_valid_move(board, 4, 4, 9)
    assert is_valid_move(board, 8, 8, 1)

def test_is_valid_move_same_row():
    board = Board()
    board.set_value(0, 1, 5)
    assert not is_valid_move(board, 0, 0, 5)

def test_is_valid_move_same_column():
    board = Board()
    board.set_value(1, 0, 5)
    assert not is_valid_move(board, 0, 0, 5)

def test_is_valid_move_same_box():
    board = Board()
    board.set_value(1, 1, 5)
    assert not is_valid_move(board, 0, 0, 5)

def test_is_valid_move_same_cell():
    board = Board()
    board.set_value(0, 0, 5)
    #placing 5 at (0,0) is valid: same cell
    assert is_valid_move(board, 0, 0, 5)

def test_is_valid_move_invalid_value():
    board = Board()
    assert not is_valid_move(board, 0, 0, 0)
    assert not is_valid_move(board, 0, 0, 10)
    assert not is_valid_move(board, 0, 0, -1)

def test_get_possible_values_empty_board():
    board = Board()
    values = get_possible_values(board, 0, 0)
    assert values == [1, 2, 3, 4, 5, 6, 7, 8, 9]

def test_get_possible_values_with_constraints():
    board = Board()
    board.set_value(0, 1, 1)
    board.set_value(0, 2, 2)
    board.set_value(1, 0, 3)
    board.set_value(1, 1, 4)

    values = get_possible_values(board, 0, 0)
    assert 1 not in values  #row
    assert 2 not in values  #row
    assert 3 not in values  #column
    assert 4 not in values  #box
    assert 5 in values

def test_get_possible_values_filled_cell():
    board = Board()
    board.set_value(0, 0, 5)
    values = get_possible_values(board, 0, 0)
    assert values == []

def test_is_board_valid_empty():
    board = Board()
    assert is_board_valid(board)


def test_is_board_valid_with_values():
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
    assert is_board_valid(board)

def test_is_board_valid_duplicate_row():
    board = Board()
    board.set_value(0, 0, 5)
    board.set_value(0, 1, 5)  #duplicate
    assert not is_board_valid(board)

def test_is_board_valid_duplicate_column():
    board = Board()
    board.set_value(0, 0, 5)
    board.set_value(1, 0, 5)  #duplicate
    assert not is_board_valid(board)

def test_is_board_valid_duplicate_box():
    board = Board()
    board.set_value(0, 0, 5)
    board.set_value(1, 1, 5)  #duplicate
    assert not is_board_valid(board)

def test_is_solved_empty_board():
    board = Board()
    assert not is_solved(board)

def test_is_solved_valid_complete():
    solved_grid = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]
    board = Board(solved_grid)
    assert is_solved(board)

def test_is_solved_invalid_complete():
    grid = [[5] * 9 for _ in range(9)] #full but invalid
    board = Board(grid)
    assert board.is_full()
    assert not is_solved(board)