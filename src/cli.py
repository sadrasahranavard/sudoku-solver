import argparse
import sys
from src.models.board import Board
from src.solver.backtracking import solve, count_solutions
from src.solver.validator import is_board_valid, is_solved
from src.generator.puzzle_gen import generate_puzzle
from src.io.file_handler import read_puzzle, write_puzzle
from src.io.display import print_board, print_comparison

#python -m src.cli puzzle.txt
#python -m src.cli puzzle.txt -o out
#python -m src.cli --generate
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

    args = parser.parse_args()

    #show help
    if not args.file and not args.generate:
        parser.print_help()
        return

    try:
        if args.generate:
            cmd_generate(args)
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
        print("\n❌ Invalid: rule violations")
        sys.exit(1)

    if is_solved(board):
        print("\n✅ Valid and solved")
        return

    solutions = count_solutions(board, limit=2)
    if solutions == 0:
        print("\n❌ Unsolvable")
    elif solutions == 1:
        print("\n✅ Valid with unique solution")
    else:
        print(f"\n✅ Valid with multiple solutions")

if __name__ == '__main__':
    main()