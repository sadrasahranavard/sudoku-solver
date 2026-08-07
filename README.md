# Sudoku Solver

A Sudoku solver and generator built with Python. Available in three versions: CLI, GUI, and Web.

---

## Versions

| Branch | Interface | Description |
|--------|-----------|-------------|
| `cli-version` | Terminal | Command-line tool with full feature set |
| `gui-version` | Desktop | Tkinter application with dark/light theme |
| `web-version` | Browser | Flask web app with responsive design |

All versions share the same core solver engine.

---

## Features (All Versions)

- Solve 9x9 Sudoku puzzles
- Validate puzzles for rule violations
- Detect unsolvable puzzles and puzzles with multiple solutions
- Generate new puzzles at three difficulty levels (easy, medium, hard)
- Manual puzzle entry with input validation
- Save and load puzzles from text files
- Pretty-printed board display

---

## CLI Version

Branch: `cli-version`

A fast, no-dependency command-line tool. Ideal for scripting, batch processing, and terminal enthusiasts.

### Usage

```bash
git checkout cli-version
python -m src.cli puzzle.txt
python -m src.cli --generate --difficulty hard
python -m src.cli --enter
python -m src.cli --validate puzzle.txt
pytest tests/ -v
```

80+ tests covering all modules.

---

## GUI Version

Branch: `gui-version`

A desktop application built with Tkinter. Features a dark/light theme toggle, menu bar with keyboard shortcuts, real-time input validation, and a status bar. Designed to feel like a native desktop tool.

### Usage

```bash
git checkout gui-version
python -m src.gui
```

### GUI-Specific Features

- Dark and light themes with full UI rebuild on toggle
- Menu bar: File (Open, Save, Exit), Puzzle (Solve, Validate, Check Solutions, Generate by difficulty, Clear), View (Theme toggle), Help (Shortcuts, About)
- Keyboard shortcuts: F5 (Solve), Ctrl+O (Open), Ctrl+S (Save), Ctrl+G (Generate), Ctrl+L (Clear)
- Real-time input filtering — only digits 1-9 accepted
- Status bar with contextual feedback
- Given cells in white, solved cells in blue
- Thick 3x3 box borders

---

## Web Version

Branch: `web-version`

A Flask-based web application with a responsive two-column layout. Controls panel on the left, Sudoku board on the right. Styled with a custom dark theme (light mode available) using CSS custom properties. Includes animated alert messages, custom dropdown styling, and a large decorative quote mark on the Maki Kaji quote.

### Installation

```bash
git checkout web-version
pip install flask
```

### Usage

```bash
python -m src.web.app
```

Open http://127.0.0.1:5000 in your browser.

### Web-Specific Features

- Responsive two-column layout: controls sidebar + board
- Dark and light themes via CSS custom properties
- Animated alert messages for success, error, and info states
- Custom-styled difficulty dropdown with SVG arrow
- File upload and download support
- Maki Kaji quote with decorative styling
- Mobile-responsive with breakpoints at 900px and 640px
- Hover and focus states on all interactive elements
- Board cells with focus ring and z-index layering

---

## Installation (Any Version)

```bash
git clone https://github.com/sadrasahranavard/sudoku-solver.git
cd sudoku-solver
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Input File Format

Plain `.txt` file, 9 rows, 9 space-separated values each. `0` or `.` for empty cells.

```
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
```

---

## Running Tests

```bash
pytest tests/ -v
```

80+ tests across 8 test files covering all core modules.

---

## Project Structure

```
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
│   ├── gui.py
│   ├── cli.py
│   └── web/
│       ├── app.py
│       ├── templates/
│       │   └── index.html
│       └── static/
│           └── style.css
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
```

---

## Algorithm

Recursive backtracking with constraint propagation.

1. Validate board for rule violations before solving
2. Find first empty cell
3. Try values 1-9, checking row/column/box constraints
4. Recursively fill next cell
5. Backtrack if stuck
6. Count solutions (0, 1, or multiple) up to a limit

---

## Known Limitations

- Empty board solving requires MRV heuristic for reasonable performance
- Hard puzzle generation is computationally expensive
- Terminal colors may not display on all systems
- Only supports standard 9x9 Sudoku

---

## Credits

Quote by Maki Kaji, Godfather of Sudoku (1951-2021), founder of Nikoli Co., Ltd. and the person who named "Sudoku."
