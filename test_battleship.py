import pytest
from battleship import Board, CellState

def test_board_initialization():
    board = Board(size=10)
    assert board.size == 10
    assert all(cell == CellState.EMPTY for row in board.grid for cell in row)

if __name__ == "__main__":
    pytest.main()
