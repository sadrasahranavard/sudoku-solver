import pytest
from src.models.cell import Cell

def test_create_empty_cell():
    cell = Cell(0, 0)
    assert cell.value == 0
    assert not cell.locked
    assert cell.is_empty()
    assert not cell.is_filled()

def test_create_filled_cell():
    cell = Cell(0, 0, value=5)
    assert cell.value == 5
    assert not cell.locked
    assert not cell.is_empty()
    assert cell.is_filled()

def test_create_locked_cell():
    cell = Cell(0, 0, value=7, locked=True)
    assert cell.value == 7
    assert cell.locked
    assert not cell.is_empty()

def test_cell_position():
    cell = Cell(4, 5)
    assert cell.row == 4
    assert cell.col == 5
    assert cell.box == 4  #(4//3)*3 + (5//3)

def test_box_calculation():
    #top left
    assert Cell(0, 0).box == 0
    assert Cell(2, 2).box == 0
    #top middle
    assert Cell(0, 3).box == 1
    #top right
    assert Cell(0, 8).box == 2
    #center
    assert Cell(4, 4).box == 4
    #bottom right
    assert Cell(8, 8).box == 8

def test_invalid_value_raises_error():
    cell = Cell(0, 0)
    with pytest.raises(ValueError, match="value must be between 0 and 9"):
        cell.value = 10
    with pytest.raises(ValueError, match="value must be between 0 and 9"):
        cell.value = -1

def test_locked_cell_cannot_be_modified():
    cell = Cell(0, 0, value=5, locked=True)
    assert cell.locked

    with pytest.raises(ValueError, match="cannot modify a locked cell"):
        cell.value = 7

    assert cell.value == 5  # Unchanged

def test_unlocked_cell_can_be_modified():
    cell = Cell(0, 0, value=5, locked=False)
    cell.value = 7
    assert cell.value == 7

def test_set_value_to_zero():
    cell = Cell(0, 0, value=5, locked=False)
    cell.value = 0
    assert cell.is_empty()
    assert not cell.is_filled()

def test_string_representation():
    assert str(Cell(0, 0)) == "."
    assert str(Cell(0, 0, value=5)) == "5"
    assert str(Cell(0, 0, value=9)) == "9"

def test_repr():
    cell = Cell(2, 3, value=5, locked=True)
    assert "row=2" in repr(cell)
    assert "col=3" in repr(cell)
    assert "value=5" in repr(cell)
    assert "locked=True" in repr(cell)