# Sudoku Solver

A Sudoku solver and generator with a command-line interface. Built with Python.

---

## Features

- Solve 9x9 Sudoku puzzles from text files
- Validate puzzles for rule violations before solving
- Detect unsolvable puzzles and puzzles with multiple solutions
- Display formatted board with box borders in the terminal
- Save solutions to file
- Generate new puzzles with guaranteed unique solutions at three difficulty levels (easy, medium, hard)
- Manual entry - type a puzzle directly in the terminal with input validation
- Multiple solution detection - reports whether a puzzle has 0, 1, or multiple solutions
- Side-by-side comparison - view original puzzle and solution together

---

## Installation

Prerequisites: Python 3.8 or higher

git clone https://github.com/sadrasahranavard/sudoku-solver.git
cd sudoku-solver
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

---

## Usage

Solve a puzzle from file:
python -m src.cli puzzle.txt

Solve and save to file:
python -m src.cli puzzle.txt -o solution.txt

Generate a new puzzle:
python -m src.cli --generate --difficulty easy
python -m src.cli --generate --difficulty medium
python -m src.cli --generate --difficulty hard

Enter a puzzle manually:
python -m src.cli --enter

Type 9 rows. Supports spaces (5 3 0 0 7 0 0 0 0) or dots (5 3 . . 7 . . . .). Validates input with retry on errors.

Validate without solving:
python -m src.cli --validate puzzle.txt

---

## Running Tests

pytest tests/ -v

80+ tests across 8 test files covering all modules.

---

## Input File Format

Plain .txt file, 9 rows, 9 space-separated values each. 0 or . for empty.

Example:

5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9

---

## Project Structure

sudoku-solver/
├── src/
│   ├── models/
│   │   ├── cell.py
│   │   └── board.py
│   ├── solver/
│   │   ├── validator.py
│   │   └── backtracking.py
│   ├── generator/
│   │   └── puzzle_gen.py
│   ├── io/
│   │   ├── file_handler.py
│   │   └── display.py
│   └── cli.py
├── tests/
│   ├── test_cell.py
│   ├── test_board.py
│   ├── test_validator.py
│   ├── test_solver.py
│   ├── test_generator.py
│   ├── test_file_handler.py
│   ├── test_display.py
│   └── test_cli.py
├── README.md
├── requirements.txt
├── setup.py
└── .gitignore

---

## Algorithm

Recursive backtracking with constraint propagation:

1. Validate board for rule violations before solving
2. Find first empty cell
3. Try values 1-9, checking row/column/box constraints
4. Recursively fill next cell
5. Backtrack if stuck
6. Can count solutions (0, 1, or multiple) up to a limit

---

## Design Decisions

- Cells track their own row, column, and box index
- Original puzzle cells are locked (cannot be modified)
- Separate modules for validation, solving, generation, I/O, and display
- Pure functions over classes for solver and validator

---

## Known Limitations

- Empty board solving skipped in tests (needs MRV heuristic)
- Hard puzzle generation takes several minutes
- Terminal colors may not work on all systems
- Only supports standard 9x9 Sudoku

---

## Future Plans

- GUI version using Tkinter (gui-version branch)
- Web version using Flask (web-version branch)

Both will share the same core solver engine.
