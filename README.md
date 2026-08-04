# Sudoku Solver

A Sudoku solver and generator with a command-line interface. Built with Python.

---

## Features

- Solve 9x9 Sudoku puzzles from text files
- Validate puzzles for rule violations before solving
- Detect unsolvable puzzles and puzzles with multiple solutions
- Display formatted board with box borders in the terminal
- Save solutions to file
- Generate new puzzles at three difficulty levels (easy, medium, hard)
- Manual entry with input validation
- Multiple solution detection
- Side-by-side puzzle and solution view

---

## Installation

Python 3.8 or higher required.

Clone the repo:
  git clone https://github.com/sadrasahranavard/sudoku-solver.git
  cd sudoku-solver

Setup virtual environment:
  python -m venv venv
  venv\Scripts\activate

Install:
  pip install -r requirements.txt

---

## Usage

Solve:
  python -m src.cli puzzle.txt

Solve and save:
  python -m src.cli puzzle.txt -o solution.txt

Generate:
  python -m src.cli --generate --difficulty easy
  python -m src.cli --generate --difficulty medium
  python -m src.cli --generate --difficulty hard

Manual entry:
  python -m src.cli --enter

Validate:
  python -m src.cli --validate puzzle.txt

---

## Running Tests

  pytest tests/ -v

80+ tests across 8 files.

---

## Input File Format

Plain .txt file. 9 rows. 9 space-separated values per row.
0 or . for empty cells.

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

  src/
    models/
      cell.py
      board.py
    solver/
      validator.py
      backtracking.py
    generator/
      puzzle_gen.py
    io/
      file_handler.py
      display.py
    cli.py

  tests/
    test_cell.py
    test_board.py
    test_validator.py
    test_solver.py
    test_generator.py
    test_file_handler.py
    test_display.py
    test_cli.py

  README.md
  requirements.txt
  setup.py
  .gitignore

---

## Algorithm

Recursive backtracking with constraint propagation:

1. Validate board before solving
2. Find first empty cell
3. Try values 1-9, check row/column/box
4. Recurse to next cell
5. Backtrack if stuck
6. Count solutions (0, 1, multiple)

---

## Design

- Cells know their row, column, box
- Given cells are locked
- Separate modules per responsibility
- Pure functions for solver and validator

---

## Limitations

- Empty board test skipped (needs MRV)
- Hard generation is slow
- Colors may not work on all terminals
- 9x9 only

---

## Future

- GUI version (Tkinter) on gui-version branch
- Web version (Flask) on web-version branch

Same core engine across all versions.
