from src.models.board import Board

def read_puzzle(filepath: str) -> Board:
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")

    #remove empty lines & strip whitespace
    lines = [line.strip() for line in lines if line.strip()]

    if len(lines) != 9:
        raise ValueError(f"Expected 9 rows of data, got {len(lines)}")

    grid = []
    for row_num, line in enumerate(lines):
        #replace dots with zeros, split by whitespace
        line = line.replace('.', '0')
        parts = line.split()

        if len(parts) != 9:
            raise ValueError(
                f"Row {row_num + 1}: expected 9 values, got {len(parts)}"
            )

        try:
            row = [int(x) for x in parts]
        except ValueError:
            raise ValueError(
                f"Row {row_num + 1}: contains non-numeric values"
            )

        for col, value in enumerate(row):
            if not (0 <= value <= 9):
                raise ValueError(
                    f"Row {row_num + 1}, column {col + 1}: "
                    f"value {value} out of range (0-9)"
                )

        grid.append(row)

    return Board(grid)

def write_puzzle(board: Board, filepath: str) -> None:
    with open(filepath, 'w', encoding='utf-8') as file:
        for row in range(9):
            values = [str(board.get_value(row, col)) for col in range(9)]
            file.write(' '.join(values) + '\n')

def board_to_string(board: Board) -> str:
    lines = []
    for row in range(9):
        values = [str(board.get_value(row, col)) for col in range(9)]
        lines.append(' '.join(values))
    return '\n'.join(lines)