from src.models.board import Board
from src.solver.validator import is_valid_move

def solve(board: Board) -> bool:
    #find first empty cell
    empty = None
    for row in range(9):
        for col in range(9):
            if board.is_empty(row, col):
                empty = (row, col)
                break
        if empty:
            break

    #no empty cells: solved
    if empty is None:
        return True

    row, col = empty

    for value in range(1, 10):
        if is_valid_move(board, row, col, value):
            board.set_value(row, col, value)

            if solve(board):
                return True

            #backtrack
            board.set_value(row, col, 0)

    return False

def count_solutions(board: Board, limit: int = 2) -> int:
    board_copy = board.copy()
    count = 0

    def _count(b: Board) -> bool:
        nonlocal count

        if count >= limit:
            return True  # Stop searching

        #find first empty cell
        empty = None
        for row in range(9):
            for col in range(9):
                if b.is_empty(row, col):
                    empty = (row, col)
                    break
            if empty:
                break

        if empty is None:
            count += 1
            return count >= limit

        row, col = empty

        for value in range(1, 10):
            if is_valid_move(b, row, col, value):
                b.set_value(row, col, value)

                if _count(b):
                    b.set_value(row, col, 0)
                    return True

                b.set_value(row, col, 0)

        return False

    _count(board_copy)
    return count

def has_unique_solution(board: Board) -> bool:
    #check if it has exactly one solution.
    return count_solutions(board, limit=2) == 1