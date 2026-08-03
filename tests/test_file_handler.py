import pytest
import tempfile
import os
from src.models.board import Board
from src.io.file_handler import read_puzzle, write_puzzle, board_to_string

def test_read_txt():
    content = """5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(content)
        temp_path = f.name

    try:
        board = read_puzzle(temp_path)
        assert board.get_value(0, 0) == 5
        assert board.get_value(0, 2) == 0
        assert board.get_value(8, 8) == 9
    finally:
        os.unlink(temp_path)

def test_read_txt_with_dots():
    content = """. . 3 . 2 . 6 . .
9 . . 3 . 5 . . 1
. . 1 8 . 6 4 . .
. . 8 1 . 2 9 . .
7 . . . . . . . 8
. . 6 7 . 8 2 . .
. . 2 6 . 9 5 . .
8 . . 2 . 3 . . 9
. . 5 . 1 . 3 . ."""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(content)
        temp_path = f.name

    try:
        board = read_puzzle(temp_path)
        assert board.get_value(0, 2) == 3
        assert board.is_empty(0, 0)
    finally:
        os.unlink(temp_path)

def test_write_and_read_back():
    board = Board()
    board.set_value(0, 0, 5)
    board.set_value(4, 4, 9)

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_path = f.name

    try:
        write_puzzle(board, temp_path)
        loaded = read_puzzle(temp_path)
        assert loaded.get_value(0, 0) == 5
        assert loaded.get_value(4, 4) == 9
        assert loaded.is_empty(1, 1)
    finally:
        os.unlink(temp_path)

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_puzzle('nonexistent_file.txt')

def test_invalid_row_count():
    content = "1 2 3 4 5 6 7 8 9"  #one row

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(content)
        temp_path = f.name

    try:
        with pytest.raises(ValueError):
            read_puzzle(temp_path)
    finally:
        os.unlink(temp_path)

def test_invalid_column_count():
    content = "1 2 3\n" * 9  #3 columns

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(content)
        temp_path = f.name

    try:
        with pytest.raises(ValueError):
            read_puzzle(temp_path)
    finally:
        os.unlink(temp_path)

def test_invalid_characters():
    content = "a b c d e f g h i\n" * 9

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(content)
        temp_path = f.name

    try:
        with pytest.raises(ValueError):
            read_puzzle(temp_path)
    finally:
        os.unlink(temp_path)

def test_read_with_empty_lines():
    content = """
5 3 0 0 7 0 0 0 0

6 0 0 1 9 5 0 0 0

0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(content)
        temp_path = f.name

    try:
        board = read_puzzle(temp_path)
        assert board.get_value(0, 0) == 5
    finally:
        os.unlink(temp_path)

def test_board_to_string():
    """Test converting board to string."""
    board = Board()
    board.set_value(0, 0, 5)
    board.set_value(0, 1, 3)

    result = board_to_string(board)
    assert result.startswith("5 3 0 0 0 0 0 0 0")