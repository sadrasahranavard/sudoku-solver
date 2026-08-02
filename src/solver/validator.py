#checking Sudoku rules
from typing import List
from src.models.board import Board

def is_valid_move(board: Board, row: int, col: int, value: int) -> bool:
    if not (1 <= value <= 9):
        return False

    #check row
    for c in range(9):
        if c != col and board.get_value(row, c) == value:
            return False

    #check column
    for r in range(9):
        if r != row and board.get_value(r, col) == value:
            return False

    #check box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r != row or c != col) and board.get_value(r, c) == value:
                return False

    return True

def get_possible_values(board: Board, row: int, col: int) -> List[int]:
    if not board.is_empty(row, col):
        return []

    return [v for v in range(1, 10) if is_valid_move(board, row, col, v)]

def is_board_valid(board: Board) -> bool:
    #check all rows
    for row in range(9):
        seen = set()
        for col in range(9):
            value = board.get_value(row, col)
            if value != 0:
                if value in seen:
                    return False
                seen.add(value)

    #check all columns
    for col in range(9):
        seen = set()
        for row in range(9):
            value = board.get_value(row, col)
            if value != 0:
                if value in seen:
                    return False
                seen.add(value)

    #check all boxes
    for box_row in (0, 3, 6):
        for box_col in (0, 3, 6):
            seen = set()
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    value = board.get_value(r, c)
                    if value != 0:
                        if value in seen:
                            return False
                        seen.add(value)

    return True

def is_solved(board: Board) -> bool:
    return board.is_full() and is_board_valid(board)