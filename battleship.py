import random
from enum import Enum
from typing import List, Tuple, Set, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

class GameAborted(Exception):
    """Exception raised when game is aborted."""
    pass

class CellState(Enum):
    """Represents the state of a cell on the board."""
    EMPTY = "."
    SHIP = "S"
    HIT = "X"
    MISS = "O"

@dataclass
class Ship:
    """Represents a ship on the board."""
    size: int
    name: str
    coordinates: Set[Tuple[int, int]] = None
    hits: Set[Tuple[int, int]] = None
    
    def __post_init__(self):
        """Initializes coordinates and hits as empty sets."""
        self.coordinates = set()
        self.hits = set()

    @property
    def is_sunk(self) -> bool:
        """Returns True if the ship is completely sunk."""
        return len(self.hits) == self.size

class Board:
    """Represents the game board."""
    def __init__(self, size: int = 10):
        """Initializes the board with the given size and an empty grid."""
        if not 10 <= size <= 15:
            raise ValueError("Board size must be between 10 and 15")
        self.size = size
        self.grid = [[CellState.EMPTY for _ in range(size)] for _ in range(size)]
        self.ships: List[Ship] = []
        
    def place_ship(self, ship: Ship, start_row: int, start_col: int, is_horizontal: bool) -> bool:
        """Places a ship on the board if valid. Returns True if successful."""
        if not self._are_coordinates_valid(start_row, start_col):
            return False
            
        coordinates = self._get_ship_coordinates(ship.size, start_row, start_col, is_horizontal)
        if not coordinates:
            return False
            
        for row, col in coordinates:
            self.grid[row][col] = CellState.SHIP
        ship.coordinates = set(coordinates)
        self.ships.append(ship)
        return True
    
    def _are_coordinates_valid(self, row: int, col: int) -> bool:
        """Checks if a cell's coordinates are within the board's bounds."""
        return 0 <= row < self.size and 0 <= col < self.size
    
    def _get_ship_coordinates(self, size: int, start_row: int, start_col: int, is_horizontal: bool) -> List[Tuple[int, int]]:
        """Generates the coordinates for a ship if the placement is valid."""
        coordinates = []
        for i in range(size):
            row = start_row if is_horizontal else start_row + i
            col = start_col + i if is_horizontal else start_col
            
            if not self._are_coordinates_valid(row, col):
                return []
            if self.grid[row][col] != CellState.EMPTY:
                return []
                
            # Check adjacent cells
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    adj_row, adj_col = row + dx, col + dy
                    if (self._are_coordinates_valid(adj_row, adj_col) and 
                        self.grid[adj_row][adj_col] == CellState.SHIP and 
                        (adj_row, adj_col) not in coordinates):
                        return []
                        
            coordinates.append((row, col))
        return coordinates

    def receive_attack(self, row: int, col: int) -> Tuple[bool, Optional[Ship]]:
        """Processes an attack at the specified cell. Returns (hit_status, ship)."""
        if not self._are_coordinates_valid(row, col):
            return False, None
            
        cell = self.grid[row][col]
        if cell in (CellState.HIT, CellState.MISS):
            return False, None
            
        is_hit = cell == CellState.SHIP
        self.grid[row][col] = CellState.HIT if is_hit else CellState.MISS
        
        if is_hit:
            for ship in self.ships:
                if (row, col) in ship.coordinates:
                    ship.hits.add((row, col))
                    return True, ship
        return True, None

    def display(self, hide_ships: bool = False) -> str:
        """Displays the board. Ships can be hidden for the opponent's view."""
        header = "   " + " ".join(f"{i:2d}" for i in range(self.size))
        rows = [header]
        
        for i, row in enumerate(self.grid):
            cells = []
            for cell in row:
                if hide_ships and cell == CellState.SHIP:
                    cells.append(CellState.EMPTY.value)
                else:
                    cells.append(cell.value)
            rows.append(f"{i:2d} {' '.join(cells)}")
        return "\n".join(rows)

class Player(ABC):
    """Abstract base class for a player."""
    @abstractmethod
    def get_move(self, board_size: int) -> Tuple[int, int]:
        pass

class HumanPlayer(Player):
    """Represents a human player."""
    def __init__(self, player_num: int):
        """Initializes the human player with a player number."""
        self.player_num = player_num

    def get_move(self, board_size: int) -> Tuple[int, int]:
        """Prompts the user for their move."""
        while True:
            try:
                print(f"\nPlayer {self.player_num}'s turn!")
                row = int(input(f"Enter attack row (0-{board_size-1}): "))
                col = int(input(f"Enter column (0-{board_size-1}): "))
                return row, col
            except ValueError:
                print("Invalid input! Please enter valid numbers.")

class ComputerPlayer(Player):
    """Represents a computer opponent."""
    def __init__(self):
        """Initializes the computer player with an empty history of previous hits."""
        self.previous_hits: Set[Tuple[int, int]] = set()
        self.potential_targets: List[Tuple[int, int]] = []

    def get_move(self, board_size: int) -> Tuple[int, int]:
        """Generates a move for the computer."""
        if self.potential_targets:
            return self.potential_targets.pop(0)
            
        while True:
            row = random.randint(0, board_size - 1)
            col = random.randint(0, board_size - 1)
            if (row, col) not in self.previous_hits:
                self.previous_hits.add((row, col))
                return row, col

class BattleshipGame:
    """Handles the main game logic."""
    SHIPS = [
        (5, "Carrier"),
        (4, "Battleship"),
        (3, "Cruiser"),
        (3, "Submarine"),
        (2, "Destroyer")
    ]
    
    def __init__(self, grid_size: int, is_two_player: bool):
        """Initializes the game with the given grid size and player mode."""
        self.grid_size = grid_size
        self.player1_board = Board(grid_size)
        self.player2_board = Board(grid_size)
        self.player1 = HumanPlayer(1)
        self.player2 = HumanPlayer(2) if is_two_player else ComputerPlayer()
        self.is_aborted = False
        
    def abort_game(self):
        """Aborts the game."""
        self.is_aborted = True
        raise GameAborted("Game aborted by player!")

    def place_computer_ships(self):
        """Randomly places ships for the computer."""
        for size, name in self.SHIPS:
            while True:
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - 1)
                is_horizontal = random.choice([True, False])
                if self.player2_board.place_ship(Ship(size, name), row, col, is_horizontal):
                    break

    def play_turn(self, player_num: int) -> str:
        """Plays a turn for the specified player."""
        player = self.player1 if player_num == 1 else self.player2
        target_board = self.player2_board if player_num == 1 else self.player1_board
        
        row, col = player.get_move(self.grid_size)
        valid, ship = target_board.receive_attack(row, col)
        
        if not valid:
            return "Invalid attack position!"
        
        if ship:
            if ship.is_sunk:
                return f"Hit! You sunk the {ship.name}!"
            return "Hit!"
        return "Miss!"

    def is_game_over(self) -> Tuple[bool, str]:
        """Checks if the game is over. Returns (game_over_status, message)."""
        if self.is_aborted:
            return True, "Game aborted!"
            
        player1_won = all(ship.is_sunk for ship in self.player2_board.ships)
        player2_won = all(ship.is_sunk for ship in self.player1_board.ships)
        
        if player1_won:
            return True, "Congratulations! Player 1 won!"
        if player2_won:
            winner = "Player 2" if isinstance(self.player2, HumanPlayer) else "Computer"
            return True, f"Game Over! {winner} won!"
        return False, ""

    def display_boards(self, current_player: int):
        """Displays both boards for the current player."""
        if current_player == 1:
            print("\nPlayer 1's Board:")
            print(self.player1_board.display())
            print("\nOpponent's Board:")
            print(self.player2_board.display(hide_ships=True))
        else:
            print("\nPlayer 2's Board:")
            print(self.player2_board.display())
            print("\nOpponent's Board:")
            print(self.player1_board.display(hide_ships=True))
            
def play_game():
    """Main game function that handles the game setup and main loop."""
    print("Welcome to Battleship!")
    
    # Game setup
    while True:
        try:
            grid_size = int(input("Enter grid size (10-15): "))
            if 10 <= grid_size <= 15:
                break
            print("Grid size must be between 10 and 15!")
        except ValueError:
            print("Please enter a valid number!")
    
    while True:
        mode = input("Select game mode (1 for Single Player, 2 for Two Players): ")
        if mode in ['1', '2']:
            break
        print("Please enter 1 or 2!")
    
    is_two_player = mode == '2'
    try:
        game = BattleshipGame(grid_size, is_two_player)
        
        print("\nPlace your ships:")
        print("(Press Ctrl+C at any time to abort the game)")
        
        # Player 1 ship placement
        print("\nPlayer 1, place your ships:")
        for size, name in BattleshipGame.SHIPS:
            game.display_boards(1)
            while True:
                try:
                    print(f"\nPlacing {name} (size: {size})")
                    row = int(input(f"Enter row (0-{grid_size-1}): "))
                    col = int(input(f"Enter column (0-{grid_size-1}): "))
                    is_horizontal = input("Place horizontally? (y/n): ").lower() == 'y'
                    
                    if game.player1_board.place_ship(Ship(size, name), row, col, is_horizontal):
                        break
                    print("Invalid placement! Ships cannot touch and must be within bounds.")
                except ValueError:
                    print("Invalid input! Please enter valid numbers.")
        
        # Player 2 / Computer ship placement
        if is_two_player:
            print("\nPlayer 2, place your ships:")
            for size, name in BattleshipGame.SHIPS:
                game.display_boards(2)
                while True:
                    try:
                        print(f"\nPlacing {name} (size: {size})")
                        row = int(input(f"Enter row (0-{grid_size-1}): "))
                        col = int(input(f"Enter column (0-{grid_size-1}): "))
                        is_horizontal = input("Place horizontally? (y/n): ").lower() == 'y'
                        
                        if game.player2_board.place_ship(Ship(size, name), row, col, is_horizontal):
                            break
                        print("Invalid placement! Ships cannot touch and must be within bounds.")
                    except ValueError:
                        print("Invalid input! Please enter valid numbers.")
        else:
            print("\nComputer is placing ships...")
            game.place_computer_ships()
        
        # Main game loop
        current_player = 1
        while True:
            game.display_boards(current_player)
            
            try:
                if current_player == 1:
                    result = game.play_turn(1)
                else:
                    if is_two_player:
                        result = game.play_turn(2)
                    else:
                        input("\nPress Enter for computer's turn (or Ctrl+C to abort)...")
                        result = game.play_turn(2)
                        print(f"\nComputer attacked!")
                print(result)
                
                # Check for game over
                game_over, message = game.is_game_over()
                if game_over:
                    game.display_boards(current_player)
                    print(message)
                    break
                
                # Switch players
                current_player = 3 - current_player  # Switches between 1 and 2
                
            except ValueError as e:
                print(f"Error: {e}")
                continue
                
    except KeyboardInterrupt:
        print("\nGame aborted by player!")
    except GameAborted:
        print("\nGame aborted!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        print("\nThanks for playing!")

if __name__ == "__main__":
    play_game()