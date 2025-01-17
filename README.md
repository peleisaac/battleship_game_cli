# Battleship Game

A Python implementation of the classic Battleship game, featuring both single-player (vs computer) and two-player modes.

## Table of Contents
- [Features](#features)
- [How to Play](#how-to-play)
  - [Starting the Game](#starting-the-game)
  - [Ship Placement Phase](#ship-placement-phase)
  - [Playing the Game](#playing-the-game)
  - [Quick Tips](#quick-tips)
- [Installation](#installation)
- [Game Rules](#game-rules)
- [Code Structure](#code-structure)
  - [Main Classes](#main-classes)
    - [Ship](#ship)
    - [Board](#board)
    - [Player](#player-abstract-base-class)
    - [BattleshipGame](#battleshipgame)
- [Usage Example](#usage-example)
- [User Interface](#user-interface)
- [Controls](#controls)
- [Error Handling](#error-handling)
- [Development](#development)
  - [Future Improvements](#future-improvements)
  - [Contributing](#contributing)


## Features

- Customizable grid size (10x10 to 15x15)
- Single-player mode with computer opponent
- Two-player mode for head-to-head gameplay
- Ship placement validation (no adjacent ships)
- Interactive command-line interface
- Standard Battleship ship fleet

## How to Play

### Starting the Game
1. Run the game using Python:
   ```bash
   python battleship.py
   ```
2. Choose your grid size (10-15)
3. Select game mode:
   - Enter '1' for Single Player (vs Computer)
   - Enter '2' for Two Players

### Ship Placement Phase
1. Player 1 places their ships first:
   - For each ship, you'll need to enter:
     - Starting row number (0-9 for 10x10 grid)
     - Starting column number (0-9 for 10x10 grid)
     - Orientation (y/n for horizontal placement)
   - The game will show you the board after each placement
   - Ships cannot touch each other, even diagonally

2. Second player/Computer places ships:
   - In two-player mode: Player 2 follows the same process
   - In single-player mode: Computer automatically places ships

### Playing the Game
1. Players take turns attacking:
   - Enter row number to attack
   - Enter column number to attack
   - The game shows the result:
     - "Miss!" - No ship at location
     - "Hit!" - Successfully hit a ship
     - "Hit! You sunk the [ship name]!" - Ship completely destroyed

2. Board Display:
   - Your board shows:
     - `.` - Empty water
     - `S` - Your ships
     - `X` - Hits (on either board)
     - `O` - Misses (on either board)
   - Opponent's board hides their ships until hit

3. Game End:
   - Game continues until all ships of one player are sunk
   - Winner is announced
   - Press Ctrl+C at any time to quit

### Quick Tips
- Write down coordinates of your successful hits to plan your strategy
- Try to sink a ship completely once you've found it
- In single-player mode, press Enter to let computer take its turn
- Ships cannot be placed adjacent to each other (including diagonally)
- The game validates all moves and ship placements automatically

## Installation

1. Ensure you have Python 3.7+ installed
2. Clone this repository or download the battleship.py file
3. Run the game using Python:
```bash
python battleship.py
```

## Game Rules

1. Each player has a fleet of 5 ships:
   - Carrier (5 spaces)
   - Battleship (4 spaces)
   - Cruiser (3 spaces)
   - Submarine (3 spaces)
   - Destroyer (2 spaces)

2. Setup Phase:
   - Players take turns placing their ships
   - Ships can be placed horizontally or vertically
   - Ships cannot touch each other (including diagonally)
   - Ships must be placed within the grid boundaries

3. Gameplay:
   - Players take turns attacking opponent's grid
   - After each attack, the result is shown (Hit/Miss)
   - When a ship is sunk, it is announced
   - First player to sink all opponent's ships wins

## Code Structure

### Main Classes

#### Ship
Represents a ship in the game.
```python
Ship(size: int, name: str)
```
- Properties:
  - `size`: Length of the ship
  - `name`: Name of the ship
  - `coordinates`: Set of coordinates occupied by the ship
  - `hits`: Set of coordinates where ship has been hit
  - `is_sunk`: Boolean indicating if ship is sunk

#### Board
Manages the game board and ship placement.
```python
Board(size: int = 10)
```
- Methods:
  - `place_ship()`: Place a ship on the board
  - `receive_attack()`: Process an attack on the board
  - `display()`: Show the current board state

#### Player (Abstract Base Class)
Base class for player implementations.
- Subclasses:
  - `HumanPlayer`: Handles human player moves
  - `ComputerPlayer`: Implements computer player logic

#### BattleshipGame
Main game controller.
```python
BattleshipGame(grid_size: int, is_two_player: bool)
```
- Methods:
  - `play_turn()`: Handle a player's turn
  - `place_computer_ships()`: Place ships for computer player
  - `is_game_over()`: Check if game has ended
  - `display_boards()`: Show game boards

## Usage Example

```python
if __name__ == "__main__":
    play_game()
```

## User Interface

The game uses a text-based interface:
- `.` represents empty cells
- `S` represents ship positions
- `X` represents hits
- `O` represents misses

Example board display:
```
   0 1 2 3 4 5 6 7 8 9
0  . . . S S S S S . .
1  . . . . . . . . . .
2  . S S S . . . . . .
3  . . . . . . . . . .
```

## Controls

- Grid coordinates are entered as row and column numbers
- Ship placement requires:
  - Starting row
  - Starting column
  - Orientation (horizontal/vertical)
- Press Ctrl+C at any time to abort the game

## Error Handling

The game handles various error conditions:
- Invalid grid coordinates
- Invalid ship placements
- Input validation
- Game abortion
- Unexpected errors

## Development

### Future Improvements
- Add save/load game functionality
- Implement different difficulty levels for computer player
- Add graphical user interface
- Include game statistics tracking
- Support for custom ship configurations
- Network play capabilities

### Contributing
Feel free to fork this repository and submit pull requests for any improvements.

