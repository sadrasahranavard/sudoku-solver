from src.models.board import Board
#color codes
BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def format_board(board: Board, show_empty_as: str = '.') -> str:
    result = []
    result.append("+-------+-------+-------+")

    for row in range(9):
        row_str = "| "
        for col in range(9):
            value = board.get_value(row, col)

            if value == 0:
                cell_str = show_empty_as
            elif board.is_locked(row, col):
                cell_str = f"{BOLD}{value}{RESET}"
            else:
                cell_str = f"{GREEN}{value}{RESET}"

            row_str += cell_str + (" | " if col % 3 == 2 else " ")

        result.append(row_str)
        if row % 3 == 2:
            result.append("+-------+-------+-------+")

    return "\n".join(result)

def print_board(board: Board, show_empty_as: str = '.') -> None:
    print(format_board(board, show_empty_as))

def format_comparison(original: Board, solved: Board) -> str:
    lines = []
    lines.append(f"{'ORIGINAL':^37}    {'SOLVED':^37}")
    lines.append("=" * 80)

    for row in range(9):
        #original
        left = "| "
        for col in range(9):
            val = original.get_value(row, col)
            left += (str(val) if val != 0 else ".") + (" | " if col % 3 == 2 else " ")

        #solved
        right = "| "
        for col in range(9):
            val = solved.get_value(row, col)
            if original.is_empty(row, col):
                right += f"{GREEN}{val}{RESET}" + (" | " if col % 3 == 2 else " ")
            else:
                right += f"{BLUE}{val}{RESET}" + (" | " if col % 3 == 2 else " ")

        lines.append(f"{left:<37}    {right}")

        if row % 3 == 2:
            lines.append("-" * 80)

    return "\n".join(lines)

def print_comparison(original: Board, solved: Board) -> None:
    print(format_comparison(original, solved))

def clear_screen() -> None:
    import os
    os.system('cls' if os.name == 'nt' else 'clear')