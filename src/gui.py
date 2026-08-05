import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.models.board import Board
from src.solver.backtracking import solve, count_solutions
from src.solver.validator import is_board_valid, is_solved
from src.generator.puzzle_gen import generate_puzzle
from src.io.file_handler import read_puzzle, write_puzzle

class SudokuGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku Solver/Generator")
        self.root.resizable(False, False)

        self.board = Board()
        self.original_board = None
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.status_var = tk.StringVar(value="Ready     _    See Help for shortcuts")
        self.dark_mode = True

        self._set_theme()
        self._build_menu()
        self._build_buttons()
        self._build_grid()
        self._build_statusbar()

        self.root.bind('<Control-s>', lambda e: self._solve())
        self.root.bind('<Control-g>', lambda e: self._generate())
        self.root.bind('<Control-o>', lambda e: self._load())
        self.root.bind('<Control-l>', lambda e: self._clear())

    def _set_theme(self):
        if self.dark_mode:
            self.bg = '#2b2b2b'
            self.cell_bg = '#3c3c3c'
            self.cell_fg = '#ffffff'
            self.given_fg = '#ffffff'
            self.solved_fg = '#4ec9ff'
            self.btn_bg = '#3c3c3c'
            self.btn_fg = '#ffffff'
            self.btn_active = '#505050'
            self.status_bg = '#0078d4'
            self.border_color = '#555555'
        else:
            self.bg = '#f0f0f0'
            self.cell_bg = '#ffffff'
            self.cell_fg = '#000000'
            self.given_fg = '#000000'
            self.solved_fg = '#0078d4'
            self.btn_bg = '#e0e0e0'
            self.btn_fg = '#000000'
            self.btn_active = '#cccccc'
            self.status_bg = '#0078d4'
            self.border_color = '#aaaaaa'

        self.root.configure(bg=self.bg)

    def _toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self._set_theme()

        for widget in self.root.winfo_children():
            widget.destroy()

        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self._build_menu()     
        self._build_buttons()
        self._build_grid()
        self._build_statusbar()

        if self.board:
            self._display_board(self.board)

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Puzzle", command=self._load)
        file_menu.add_command(label="Save As", command=self._save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        puzzle_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Puzzle", menu=puzzle_menu)
        puzzle_menu.add_command(label="Solve", command=self._solve)
        puzzle_menu.add_command(label="Validate", command=self._validate)
        puzzle_menu.add_command(label="Check Solutions", command=self._check_solutions)
        puzzle_menu.add_separator()
        puzzle_menu.add_command(label="Generate Easy", command=lambda: self._generate('easy'))
        puzzle_menu.add_command(label="Generate Medium", command=lambda: self._generate('medium'))
        puzzle_menu.add_command(label="Generate Hard", command=lambda: self._generate('hard'))
        puzzle_menu.add_separator()
        puzzle_menu.add_command(label="Clear Grid", command=self._clear)

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Dark/Light Mode", command=self._toggle_theme)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Shortcuts", command=self._show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self._about)

    def _build_buttons(self):
        btn_frame = tk.Frame(self.root, bg=self.bg)
        btn_frame.pack(pady=(10, 5))

        style = {
            'font': ('Segoe UI', 10),
            'width': 12,
            'bg': self.btn_bg,
            'fg': self.btn_fg,
            'relief': 'flat',
            'activebackground': self.btn_active,
            'activeforeground': self.btn_fg,
            'cursor': 'hand2'
        }

        tk.Button(btn_frame, text="Solve", command=self._solve, **style).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Validate", command=self._validate, **style).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Generate", command=lambda: self._generate('medium'), **style).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Load", command=self._load, **style).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Save", command=self._save, **style).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Clear", command=self._clear, **style).pack(side=tk.LEFT, padx=3)

        self.root.bind('<F5>', lambda e: self._solve())

    def _build_grid(self):
        grid_frame = tk.Frame(self.root, bg=self.bg, padx=10, pady=10)
        grid_frame.pack()

        for row in range(9):
            for col in range(9):
                padx = (2, 2)
                pady = (2, 2)
                if col % 3 == 0:
                    padx = (6, 2)
                if col == 8:
                    padx = (2, 6)
                if row % 3 == 0:
                    pady = (6, 2)
                if row == 8:
                    pady = (2, 6)

                cell = tk.Entry(
                    grid_frame,
                    width=2,
                    font=('Segoe UI', 20, 'bold'),
                    justify='center',
                    bg=self.cell_bg,
                    fg=self.cell_fg,
                    insertbackground=self.cell_fg,
                    relief='flat',
                    borderwidth=0,
                    highlightthickness=1,
                    highlightbackground=self.border_color,
                    highlightcolor='#0078d4'
                )
                cell.grid(row=row, column=col, padx=padx, pady=pady, ipadx=8, ipady=8)
                cell.bind('<KeyRelease>', self._on_cell_change)
                self.cells[row][col] = cell

    def _build_statusbar(self):
        status_frame = tk.Frame(self.root, bg=self.status_bg, height=25)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            bg=self.status_bg,
            fg='#ffffff',
            font=('Segoe UI', 9),
            anchor=tk.W,
            padx=10
        )
        status_label.pack(fill=tk.X)

    def _on_cell_change(self, event):
        widget = event.widget
        value = widget.get()
        if value and not (value.isdigit() and 1 <= int(value) <= 9):
            widget.delete(0, tk.END)

    def _read_grid(self):
        grid = []
        for row in range(9):
            grid_row = []
            for col in range(9):
                val = self.cells[row][col].get().strip()
                grid_row.append(int(val) if val.isdigit() and 1 <= int(val) <= 9 else 0)
            grid.append(grid_row)
        return grid

    def _display_board(self, board, show_original=True):
        for row in range(9):
            for col in range(9):
                value = board.get_value(row, col)
                cell = self.cells[row][col]
                cell.delete(0, tk.END)
                if value != 0:
                    cell.insert(0, str(value))
                    if board.is_locked(row, col):
                        cell.config(fg=self.given_fg, font=('Segoe UI', 20, 'bold'))
                    else:
                        cell.config(fg=self.solved_fg, font=('Segoe UI', 20, 'bold'))
                else:
                    cell.config(fg=self.cell_fg, font=('Segoe UI', 20, 'bold'))

    def _solve(self):
        grid = self._read_grid()
        try:
            self.board = Board(grid)
            self.original_board = Board(grid)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        if not is_board_valid(self.board):
            messagebox.showerror("Invalid Puzzle", "This puzzle contains rule violations!")
            self.status_var.set("Invalid puzzle")
            return
        if is_solved(self.board):
            messagebox.showinfo("Already Solved", "This puzzle is already solved!")
            self.status_var.set("Already solved")
            return
        self.status_var.set("Solving...")
        self.root.update()
        if solve(self.board):
            self._display_board(self.board)
            self.status_var.set("Solved successfully!")
        else:
            messagebox.showerror("Unsolvable", "No solution exists for this puzzle!")
            self.status_var.set("No solution exists")

    def _validate(self):
        grid = self._read_grid()
        try:
            self.board = Board(grid)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        if not is_board_valid(self.board):
            messagebox.showwarning("Invalid", "Puzzle contains rule violations!")
            self.status_var.set("Invalid puzzle")
            return
        if is_solved(self.board):
            messagebox.showinfo("Valid", "Puzzle is valid and already solved!")
            self.status_var.set("Valid and solved")
            return
        solutions = count_solutions(self.board, limit=2)
        if solutions == 0:
            messagebox.showwarning("Unsolvable", "No solution exists!")
            self.status_var.set("Unsolvable")
        elif solutions == 1:
            messagebox.showinfo("Valid", "Puzzle is valid with a unique solution!")
            self.status_var.set("Valid — unique solution")
        else:
            messagebox.showinfo("Valid", "Puzzle is valid with multiple solutions!")
            self.status_var.set("Valid — multiple solutions")

    def _check_solutions(self):
        grid = self._read_grid()
        try:
            board = Board(grid)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        if not is_board_valid(board):
            messagebox.showwarning("Invalid", "Puzzle is invalid!")
            return
        solutions = count_solutions(board, limit=3)
        if solutions == 0:
            msg = "No solutions"
        elif solutions == 1:
            msg = "Unique solution"
        elif solutions == 2:
            msg = "At least 2 solutions"
        else:
            msg = "3 or more solutions"
        messagebox.showinfo("Solution Count", msg)
        self.status_var.set(msg)

    def _generate(self, difficulty='medium'):
        self._clear()
        self.status_var.set(f"Generating {difficulty} puzzle...")
        self.root.update()
        puzzle, _ = generate_puzzle(difficulty)
        self.board = puzzle
        self.original_board = puzzle.copy()
        self._display_board(puzzle)
        empty = len(puzzle.get_empty_positions())
        self.status_var.set(f"Generated {difficulty} puzzle — {empty} empty cells")

    def _load(self):
        filepath = filedialog.askopenfilename(
            title="Open Puzzle",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return
        try:
            self.board = read_puzzle(filepath)
            self.original_board = self.board.copy()
            self._display_board(self.board)
            self.status_var.set(f"Loaded: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Failed to load file")

    def _save(self):
        filepath = filedialog.asksaveasfilename(
            title="Save Puzzle",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if not filepath:
            return
        try:
            write_puzzle(self.board, filepath)
            self.status_var.set(f"Saved to: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Failed to save file")

    def _clear(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].delete(0, tk.END)
                self.cells[row][col].config(fg=self.cell_fg)
        self.board = Board()
        self.original_board = None
        self.status_var.set("Grid cleared")

    def _about(self):
        messagebox.showinfo(
            "About Sudoku Solver",
            "Sudoku Solver v2.0\n\n"
            "Solve, validate, and generate Sudoku puzzles.\n\n"
            "Built with Python and Tkinter."
        )

    def _show_shortcuts(self):
        messagebox.showinfo(
            "Keyboard Shortcuts",
            "F5     —     Solve puzzle\n"
            "Ctrl+O     —    Open puzzle file\n"
            "Ctrl+S    —    Save puzzle to file\n"
            "Ctrl+G    —    Generate new puzzle\n"
            "Ctrl+L    —     Clear grid\n"
        )

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = SudokuGUI()
    app.run()