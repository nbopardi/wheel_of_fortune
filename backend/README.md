# Wheel of Fortune - Backend

A Python backend implementation of the Wheel of Fortune game designed for in-person gameplay with friends.

## Features

### Core Game Mechanics
- **Flexible Team Support**: 2-6 teams with customizable team names and member lists
- **Manual Wheel Input**: Designed for use with a physical wheel - input results manually using enum values
- **Complete Game Flow**: Turn-based gameplay, round progression, and scoring
- **Puzzle Management**: 20+ built-in puzzles across multiple categories

### Key Components

#### Models
- **Team**: Represents teams with members, money tracking, and free spin management
- **WheelResult**: Enum with all wheel options (money values and special segments)
- **Puzzle**: Handles word puzzles, letter revelation, and solution checking
- **Round**: Manages individual game rounds with puzzles and completion tracking
- **Game**: Main game controller orchestrating teams, rounds, and turn management

#### Managers
- **GameEngine**: High-level interface for all game operations
- **PuzzleManager**: Loads and manages puzzle data from JSON files
- **ScoreManager**: Handles scoring, leaderboards, and game statistics

#### Game States
- **SETUP**: Initial game creation
- **IN_PROGRESS**: Active gameplay
- **ROUND_COMPLETED**: Between rounds
- **GAME_COMPLETED**: Game finished

## Installation

No external dependencies required! The backend uses only Python standard library.

```bash
# Python 3.8+ required
python3 --version

# Navigate to backend directory
cd backend

# Run tests
python3 tests/test_basic.py

# Run demo
python3 main.py demo

# Run interactive mode
python3 main.py
```

## Usage

### Quick Start
```python
from managers.game_engine import GameEngine
from models.wheel_result import WheelResult

# Create game engine
engine = GameEngine()

# Create teams
teams = [
    {"name": "Team Alpha", "members": ["Alice", "Bob"]},
    {"name": "Team Beta", "members": ["Charlie", "Diana"]}
]

# Create and start game
result = engine.create_game(teams, total_rounds=3)
if result["success"]:
    engine.start_game()

# Process wheel spin (manual input from physical wheel)
result = engine.process_wheel_spin(WheelResult.MONEY_500)

# Process letter guess (if wheel landed on money)
if result.get("action_required") == "guess_consonant":
    letter_result = engine.process_letter_guess("T")

# Buy a vowel
vowel_result = engine.process_vowel_purchase("A")

# Attempt to solve
solve_result = engine.process_solve_attempt("HELLO WORLD")

# Get game status
status = engine.get_game_status()
```

### Wheel Options
The `WheelResult` enum includes:

**Money Values:**
- MONEY_300 ($300), MONEY_500 ($500), MONEY_550 ($550), etc.
- MONEY_2500 ($2,500), MONEY_5000 ($5,000)

**Special Segments:**
- BANKRUPT (lose all round money)
- LOSE_A_TURN (end turn)
- FREE_SPIN (get extra turn)

### Game Flow
1. **Create Game**: Set up teams and rounds
2. **Start Game**: Begin first round
3. **Team Turn**: 
   - Spin wheel (manual input)
   - Guess consonant (if money) or handle special segment
   - Optional: Buy vowel or attempt solve
4. **Round Completion**: Team solves puzzle, wins round money
5. **Next Round**: Continue until all rounds complete
6. **Game End**: Team with most total money wins

## File Structure

```
backend/
├── models/           # Core data models
├── managers/         # Business logic managers
├── utils/           # Utilities and constants
├── data/            # Puzzle data files (JSON)
├── tests/           # Unit tests
├── main.py          # Demo/CLI interface
└── requirements.txt # Dependencies (minimal)
```

## Customization

### Adding Puzzles
```python
from managers.puzzle_manager import PuzzleManager

puzzle_manager = PuzzleManager()
puzzle_manager.add_puzzle("NEW PUZZLE", "PHRASE")
```

### Custom Wheel Configuration
Modify `models/wheel_result.py` to add new money values or special segments.

## Testing

```bash
# Run all tests
python3 tests/test_basic.py

# Run interactive demo
python3 main.py
```

## Next Steps

The backend is complete and ready for frontend integration. Key integration points:

1. **GameEngine**: Main interface for all game operations
2. **WheelResult**: Enum for easy wheel option selection in UI
3. **Game Status**: Comprehensive state information for display
4. **Event Handling**: All actions return detailed result dictionaries

Ready for web, mobile, or desktop frontend development!

## Design Decisions

- **Manual Wheel Input**: Designed for physical wheel use, not random generation
- **Team-Based**: Flexible team sizes instead of fixed individual players  
- **Enum Wheel Options**: Easy frontend integration with fixed set of choices
- **Comprehensive State**: Rich game status for UI updates
- **No External Dependencies**: Pure Python for easy deployment
- **JSON Data Storage**: Simple puzzle management and customization 