import argparse
import sys
from src.models.board import Board
from src.solver.backtracking import solve, count_solutions
from src.solver.validator import is_board_valid, is_solved
from src.generator.puzzle_gen import generate_puzzle
from src.io.file_handler import read_puzzle, write_puzzle
from src.io.display import print_board, print_comparison

#python -m src.cli puzzle.txt          Solve and display
#python -m src.cli puzzle.txt -o out   Solve and save
#python -m src.cli --generate
#python -m src.cli --enter             Enter a puzzle manually
#python -m src.cli --validate puzzle

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sudoku Solver & Generator"
    )

    parser.add_argument(
        'file',
        nargs='?',
        help='Puzzle file to solve or validate'
    )
    parser.add_argument(
        '-o', '--output',
        help='Save solution to file'
    )
    parser.add_argument(
        '-g', '--generate',
        action='store_true',
        help='Generate a new puzzle'
    )
    parser.add_argument(
        '-d', '--difficulty',
        choices=['easy', 'medium', 'hard'],
        default='medium',
        help='Difficulty for generated puzzle'
    )
    parser.add_argument(
        '-v', '--validate',
        action='store_true',
        help='Validate puzzle without solving'
    )
    parser.add_argument(
        '-e', '--enter',
        action='store_true',
        help='Enter a puzzle manually via terminal'
    )

    args = parser.parse_args()

    if not args.file and not args.generate and not args.enter:
        parser.print_help()
        return

    try:
        if args.generate:
            cmd_generate(args)
        elif args.enter:
            cmd_enter(args)
        elif args.validate:
            cmd_validate(args)
        else:
            cmd_solve(args)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(1)

def cmd_solve(args) -> None:
    print(f"Loading: {args.file}")
    board = read_puzzle(args.file)

    print("\nPuzzle:")
    print_board(board)

    if not is_board_valid(board):
        print("\nError: Puzzle contains rule violations!")
        sys.exit(1)

    if is_solved(board):
        print("\nThis puzzle is already solved!")
        return

    print("\nSolving...")
    if solve(board):
        print("\nSolution:")
        print_board(board)

        if args.output:
            write_puzzle(board, args.output)
            print(f"\nSaved to: {args.output}")
    else:
        print("\nNo solution exists!")
        sys.exit(1)

def cmd_generate(args) -> None:
    print(f"Generating {args.difficulty} puzzle...\n")
    puzzle, solution = generate_puzzle(args.difficulty)

    print("Puzzle:")
    print_board(puzzle)

    empty = len(puzzle.get_empty_positions())
    print(f"\nEmpty cells: {empty}/81")

    if args.output:
        write_puzzle(puzzle, args.output)
        print(f"Saved to: {args.output}")

    print("\nPress Enter to see solution, or Ctrl+C to quit...")
    try:
        input()
        print("\nSolution:")
        print_comparison(puzzle, solution)
    except KeyboardInterrupt:
        print("\n")

def cmd_validate(args) -> None:
    print(f"Loading: {args.file}")
    board = read_puzzle(args.file)

    print("\nPuzzle:")
    print_board(board)

    if not is_board_valid(board):
        print("\nInvalid - contains rule violations!")
        sys.exit(1)

    if is_solved(board):
        print("\nValid and already solved!")
        return

    solutions = count_solutions(board, limit=2)
    if solutions == 0:
        print("\nUnsolvable!")
    elif solutions == 1:
        print("\nValid with unique solution!")
    else:
        print(f"\nValid with multiple solutions!")

def cmd_enter(args) -> None:
    print("Enter your Sudoku puzzle row by row.")
    print("Use numbers 1-9 for filled cells, 0 or . for empty cells.")
    print("Example: 5 3 0 0 7 0 0 0 0")
    print()

    lines = []
    for i in range(9):
        while True:
            try:
                line = input(f"Row {i + 1}: ").strip()
            except KeyboardInterrupt:
                print("\n\nCancelled.")
                return
            except EOFError:
                print("\n\nInput ended unexpectedly.")
                return

            if not line:
                print("  Error: Row cannot be empty. Try again.")
                continue

            line = line.replace('.', '0')
            parts = line.split()

            if len(parts) != 9:
                print(f"  Error: Expected 9 values, got {len(parts)}. Try again.")
                continue

            try:
                row = [int(x) for x in parts]
            except ValueError:
                print("  Error: All values must be numbers. Try again.")
                continue

            if any(not (0 <= v <= 9) for v in row):
                print("  Error: Values must be between 0 and 9. Try again.")
                continue

            lines.append(' '.join(str(x) for x in row))
            break

    puzzle_str = '\n'.join(lines)

    try:
        board = Board.from_string(puzzle_str)
    except ValueError as e:
        print(f"\nError: {e}")
        return

    print("\nYour puzzle:")
    print_board(board)

    if not is_board_valid(board):
        print("\nError: Puzzle contains rule violations!")
        print("(Duplicate value in a row, column, or 3x3 box)")
        return

    if is_solved(board):
        print("\nThis puzzle is already solved!")
        return

    print("\nSolving...")
    if solve(board):
        print("\nSolution:")
        print_board(board)

        if args.output:
            write_puzzle(board, args.output)
            print(f"\nSaved to: {args.output}")
    else:
        print("\nNo solution exists!")

if __name__ == '__main__':
    main()