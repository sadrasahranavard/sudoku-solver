import pytest
from src.models.board import Board
from src.io.display import (
    format_board,
    print_board,
    format_comparison,
    print_comparison,
    clear_screen,
)

def test_format_board():
    board = Board()
    board.set_value(0, 0, 5)

    formatted = format_board(board)
    assert "5" in formatted
    assert "+-------+-------+-------+" in formatted

def test_format_board_with_custom_empty():
    board = Board()
    formatted = format_board(board, show_empty_as='*')
    assert '*' in formatted

def test_format_board_shows_locked_cells():
    grid = [[5 if r == 0 and c == 0 else 0 for c in range(9)] for r in range(9)]
    board = Board(grid)

    formatted = format_board(board)
    assert "5" in formatted

def test_print_board(capsys):
    board = Board()
    board.set_value(0, 0, 5)

    print_board(board)
    captured = capsys.readouterr()
    assert "5" in captured.out

def test_format_comparison():
    original = Board()
    original.set_value(0, 0, 5)

    solved = Board()
    solved.set_value(0, 0, 5)
    solved.set_value(0, 2, 4)

    comparison = format_comparison(original, solved)
    assert "ORIGINAL" in comparison
    assert "SOLVED" in comparison
    assert "5" in comparison

def test_print_comparison(capsys):
    original = Board()
    original.set_value(0, 0, 5)

    solved = Board()
    solved.set_value(0, 0, 5)

    print_comparison(original, solved)
    captured = capsys.readouterr()
    assert "ORIGINAL" in captured.out
    assert "SOLVED" in captured.out

def test_clear_screen():
    clear_screen()

def test_format_empty_board():
    board = Board()
    formatted = format_board(board)
    assert "." in formatted
    assert "+-------+-------+-------+" in formatted

def test_format_full_board():
    board = Board()
    for r in range(9):
        for c in range(9):
            board.set_value(r, c, ((r * 3 + r // 3 + c) % 9) + 1)

    formatted = format_board(board)
    assert "." not in formatted