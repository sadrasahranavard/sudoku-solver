import pytest
from src.models.board import Board
from src.solver.backtracking import solve, count_solutions, has_unique_solution
from src.solver.validator import is_board_valid

VALID_PUZZLE = [
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

def test_solve_valid_puzzle():
    board = Board(VALID_PUZZLE)
    result = solve(board)
    assert result is True
    assert board.is_full()
    assert is_board_valid(board)

def test_solve_already_solved():
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
    result = solve(board)
    assert result is True

def test_solve_unsolvable_puzzle():
    grid = [[0] * 9 for _ in range(9)]
    grid[0][0] = 5
    grid[0][1] = 5  #duplicate
    board = Board(grid)
    result = solve(board)
    assert result is False

@pytest.mark.skip(reason="requires MRV heuristic to complete")
def test_solve_empty_board():
    board = Board()
    result = solve(board)
    assert result is True
    assert board.is_full()
    assert is_board_valid(board)

def test_count_solutions_unique():
    board = Board(VALID_PUZZLE)
    assert count_solutions(board) == 1

def test_count_solutions_empty_board():
    board = Board()
    assert count_solutions(board, limit=2) == 2

def test_count_solutions_unsolvable():
    grid = [[0] * 9 for _ in range(9)]
    grid[0][0] = 5
    grid[0][1] = 5
    board = Board(grid)
    assert count_solutions(board) == 0

def test_has_unique_solution_true():
    board = Board(VALID_PUZZLE)
    assert has_unique_solution(board) is True

def test_has_unique_solution_false():
    board = Board()
    assert has_unique_solution(board) is False

def test_solve_does_not_modify_given_cells():
    board = Board(VALID_PUZZLE)
    solve(board)
    #cells should have their values
    assert board.get_value(0, 0) == 5
    assert board.get_value(0, 1) == 3
    assert board.get_value(1, 3) == 1

def test_solve_fills_all_empty_cells():
    board = Board(VALID_PUZZLE)
    solve(board)
    empty = board.get_empty_positions()
    assert len(empty) == 0