import random
from typing import Tuple
from src.models.board import Board
from src.solver.backtracking import has_unique_solution
from src.solver.validator import is_valid_move

def generate_solution() -> Board:
    board = Board()
    _fill_board(board)
    return board

def _fill_board(board: Board) -> bool:
    empty = None
    for row in range(9):
        for col in range(9):
            if board.is_empty(row, col):
                empty = (row, col)
                break
        if empty:
            break

    if empty is None:
        return True

    row, col = empty
    values = list(range(1, 10))
    random.shuffle(values)

    for value in values:
        if is_valid_move(board, row, col, value):
            board.set_value(row, col, value)
            if _fill_board(board):
                return True
            board.set_value(row, col, 0)

    return False

def generate_puzzle(difficulty: str = 'medium') -> Tuple[Board, Board]:
    difficulty_levels = {
        'easy': 30,
        'medium': 45,
        'hard': 55,
    }

    if difficulty not in difficulty_levels:
        raise ValueError(
            f"Invalid difficulty: '{difficulty}'. "
            f"Choose from: {list(difficulty_levels.keys())}"
        )

    target_empty = difficulty_levels[difficulty]

    solution = generate_solution()

    grid = solution.to_grid()

    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)

    removed = 0
    for row, col in positions:
        if removed >= target_empty:
            break

        backup = grid[row][col]
        grid[row][col] = 0

        test_board = Board(grid)
        for r in range(9):
            for c in range(9):
                test_board._cells[r][c]._locked = False

        if has_unique_solution(test_board):
            removed += 1
        else:
            grid[row][col] = backup

    puzzle = Board(grid)
    return puzzle, solution