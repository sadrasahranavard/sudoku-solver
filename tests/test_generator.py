import pytest
from src.generator.puzzle_gen import generate_puzzle, generate_solution
from src.solver.backtracking import solve, has_unique_solution
from src.solver.validator import is_board_valid, is_solved

def test_generate_solution():
    solution = generate_solution()
    assert solution.is_full()
    assert is_board_valid(solution)
    assert is_solved(solution)


def test_generate_easy_puzzle():
    puzzle, solution = generate_puzzle('easy')
    assert is_board_valid(puzzle)
    assert solution.is_full()
    assert is_board_valid(solution)
    assert has_unique_solution(puzzle)
    puzzle_filled = 81 - len(puzzle.get_empty_positions())
    assert puzzle_filled < 81

def test_generate_medium_puzzle():
    puzzle, solution = generate_puzzle('medium')

    assert is_board_valid(puzzle)
    assert solution.is_full()
    assert is_board_valid(solution)
    assert has_unique_solution(puzzle)

def test_generate_hard_puzzle():
    puzzle, solution = generate_puzzle('hard')

    assert is_board_valid(puzzle)
    assert solution.is_full()
    assert is_board_valid(solution)
    assert has_unique_solution(puzzle)

def test_generate_invalid_difficulty():
    with pytest.raises(ValueError):
        generate_puzzle('impossible')

def test_generated_puzzle_is_solvable():
    puzzle, _ = generate_puzzle('medium')
    solved_board = puzzle.copy()
    result = solve(solved_board)
    assert result is True
    assert is_solved(solved_board)

def test_different_puzzles_are_different():
    puzzle1, _ = generate_puzzle('easy')
    puzzle2, _ = generate_puzzle('easy')
    
    grid1 = puzzle1.to_grid()
    grid2 = puzzle2.to_grid()
    
    assert grid1 != grid2

def test_difficulty_levels_have_different_empty_counts():
    easy, _ = generate_puzzle('easy')
    medium, _ = generate_puzzle('medium')
    hard, _ = generate_puzzle('hard')

    easy_empty = len(easy.get_empty_positions())
    medium_empty = len(medium.get_empty_positions())
    hard_empty = len(hard.get_empty_positions())

    assert easy_empty <= medium_empty <= hard_empty