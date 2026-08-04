import pytest
from src.cli import main

def test_cmd_enter_valid_puzzle(monkeypatch, capsys):
    inputs = [
        "5 3 0 0 7 0 0 0 0",
        "6 0 0 1 9 5 0 0 0",
        "0 9 8 0 0 0 0 6 0",
        "8 0 0 0 6 0 0 0 3",
        "4 0 0 8 0 3 0 0 1",
        "7 0 0 0 2 0 0 0 6",
        "0 6 0 0 0 0 2 8 0",
        "0 0 0 4 1 9 0 0 5",
        "0 0 0 0 8 0 0 7 9",
    ]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    import sys
    sys.argv = ['cli', '--enter']

    try:
        main()
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert "Your puzzle:" in captured.out
    assert "Solution:" in captured.out

def test_cmd_enter_invalid_row_length(monkeypatch, capsys):
    inputs = [
        "5 3 0",
        "5 3 0 0 7 0 0 0 0",
        "6 0 0 1 9 5 0 0 0",
        "0 9 8 0 0 0 0 6 0",
        "8 0 0 0 6 0 0 0 3",
        "4 0 0 8 0 3 0 0 1",
        "7 0 0 0 2 0 0 0 6",
        "0 6 0 0 0 0 2 8 0",
        "0 0 0 4 1 9 0 0 5",
        "0 0 0 0 8 0 0 7 9",
    ]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    import sys
    sys.argv = ['cli', '--enter']

    try:
        main()
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert "Expected 9 values" in captured.out

def test_cmd_enter_with_dots(monkeypatch, capsys):
    inputs = [
        ". . 3 . 2 . 6 . .",
        "9 . . 3 . 5 . . 1",
        ". . 1 8 . 6 4 . .",
        ". . 8 1 . 2 9 . .",
        "7 . . . . . . . 8",
        ". . 6 7 . 8 2 . .",
        ". . 2 6 . 9 5 . .",
        "8 . . 2 . 3 . . 9",
        ". . 5 . 1 . 3 . .",
    ]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    import sys
    sys.argv = ['cli', '--enter']

    try:
        main()
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert "Your puzzle:" in captured.out
    assert "Solution:" in captured.out

def test_cmd_enter_duplicate_in_row(monkeypatch, capsys):
    inputs = [
        "5 5 0 0 7 0 0 0 0",
        "6 0 0 1 9 5 0 0 0",
        "0 9 8 0 0 0 0 6 0",
        "8 0 0 0 6 0 0 0 3",
        "4 0 0 8 0 3 0 0 1",
        "7 0 0 0 2 0 0 0 6",
        "0 6 0 0 0 0 2 8 0",
        "0 0 0 4 1 9 0 0 5",
        "0 0 0 0 8 0 0 7 9",
    ]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    import sys
    sys.argv = ['cli', '--enter']

    try:
        main()
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert "rule violations" in captured.out

def test_cmd_enter_non_numeric(monkeypatch, capsys):
    inputs = [
        "a b c d e f g h i",
        "5 3 0 0 7 0 0 0 0",
        "6 0 0 1 9 5 0 0 0",
        "0 9 8 0 0 0 0 6 0",
        "8 0 0 0 6 0 0 0 3",
        "4 0 0 8 0 3 0 0 1",
        "7 0 0 0 2 0 0 0 6",
        "0 6 0 0 0 0 2 8 0",
        "0 0 0 4 1 9 0 0 5",
        "0 0 0 0 8 0 0 7 9",
    ]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    import sys
    sys.argv = ['cli', '--enter']

    try:
        main()
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert "All values must be numbers" in captured.out

def test_cmd_enter_empty_row(monkeypatch, capsys):
    inputs = [
        "",
        "5 3 0 0 7 0 0 0 0",
        "6 0 0 1 9 5 0 0 0",
        "0 9 8 0 0 0 0 6 0",
        "8 0 0 0 6 0 0 0 3",
        "4 0 0 8 0 3 0 0 1",
        "7 0 0 0 2 0 0 0 6",
        "0 6 0 0 0 0 2 8 0",
        "0 0 0 4 1 9 0 0 5",
        "0 0 0 0 8 0 0 7 9",
    ]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    import sys
    sys.argv = ['cli', '--enter']

    try:
        main()
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert "Row cannot be empty" in captured.out