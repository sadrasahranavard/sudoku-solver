import os
from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from src.models.board import Board
from src.solver.backtracking import solve, count_solutions
from src.solver.validator import is_board_valid, is_solved
from src.generator.puzzle_gen import generate_puzzle
from src.io.file_handler import read_puzzle, write_puzzle
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
app.secret_key = 'sudoku-solver-secret-key'

UPLOAD_FOLDER = tempfile.gettempdir()

@app.route('/', methods=['GET', 'POST'])
def index():
    board = Board()
    original = None
    action = request.form.get('action', '')
    difficulty = request.form.get('difficulty', 'medium')
    message = ''
    message_type = ''

    grid = _read_grid_from_form()

    if grid:
        try:
            board = Board(grid)
        except ValueError:
            board = Board()

    if action == 'solve':
        if not is_board_valid(board):
            message = 'Puzzle contains rule violations!'
            message_type = 'error'
        elif is_solved(board):
            message = 'Puzzle is already solved!'
            message_type = 'info'
        else:
            original = board.copy()
            if solve(board):
                message = 'Puzzle solved successfully!'
                message_type = 'success'
            else:
                message = 'No solution exists!'
                message_type = 'error'
                board = original

    elif action == 'validate':
        if not is_board_valid(board):
            message = 'Invalid — contains rule violations!'
            message_type = 'error'
        elif is_solved(board):
            message = 'Valid and already solved!'
            message_type = 'success'
        else:
            solutions = count_solutions(board, limit=2)
            if solutions == 0:
                message = 'Unsolvable!'
                message_type = 'error'
            elif solutions == 1:
                message = 'Valid with unique solution!'
                message_type = 'success'
            else:
                message = 'Valid with multiple solutions!'
                message_type = 'info'

    elif action == 'check':
        if is_board_valid(board):
            solutions = count_solutions(board, limit=3)
            if solutions == 0:
                message = 'No solutions'
            elif solutions == 1:
                message = 'Unique solution'
            elif solutions == 2:
                message = 'At least 2 solutions'
            else:
                message = '3 or more solutions'
            message_type = 'info'
        else:
            message = 'Invalid puzzle!'
            message_type = 'error'

    elif action == 'generate':
        puzzle, _ = generate_puzzle(difficulty)
        board = puzzle
        empty = len(puzzle.get_empty_positions())
        message = f'Generated {difficulty} puzzle — {empty} empty cells'
        message_type = 'success'

    elif action == 'clear':
        board = Board()
        message = 'Grid cleared'
        message_type = 'info'

    elif action == 'load':
        file = request.files.get('file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            try:
                board = read_puzzle(filepath)
                message = f'Loaded: {filename}'
                message_type = 'success'
            except Exception as e:
                message = f'Error loading file: {e}'
                message_type = 'error'
            finally:
                os.remove(filepath)

    elif action == 'save':
        if board:
            filepath = os.path.join(UPLOAD_FOLDER, 'puzzle.txt')
            write_puzzle(board, filepath)
            return send_file(filepath, as_attachment=True, download_name='puzzle.txt')

    return render_template(
        'index.html',
        board=board,
        original=original,
        message=message,
        message_type=message_type,
        difficulty=difficulty
    )

def _read_grid_from_form():
    grid = []
    for row in range(9):
        grid_row = []
        for col in range(9):
            key = f'cell_{row}_{col}'
            val = request.form.get(key, '').strip()
            if val.isdigit() and 1 <= int(val) <= 9:
                grid_row.append(int(val))
            else:
                grid_row.append(0)
        grid.append(grid_row)

    if all(all(v == 0 for v in row) for row in grid):
        return None

    return grid

if __name__ == '__main__':
    app.run(debug=True)