# Wheel of Fortune Game

A digital implementation of the popular TV game show "Wheel of Fortune" designed for in-person gameplay with friends and teams.

## Project Status

✅ **Backend Complete** - Fully functional Python backend with comprehensive game logic  
🚧 **Frontend Planned** - Ready for frontend development

## Game Features

### Designed for In-Person Play
- **Physical Wheel Support**: Manual input system for real physical wheel spins
- **Flexible Teams**: 2-6 teams with customizable names and member lists
- **Interactive Gameplay**: Perfect for parties, game nights, and group events

### Core Gameplay
- **Word Puzzles**: 20+ built-in puzzles across multiple categories
- **Money Management**: Team scoring with round-based and total money tracking
- **Special Segments**: BANKRUPT, LOSE A TURN, FREE SPIN mechanics
- **Complete Game Flow**: Multi-round games with proper turn management

## Backend Implementation

The backend is **100% complete** and includes:

### Core Models
- **Team**: Flexible team management with member tracking
- **WheelResult**: Enum-based wheel options for easy UI integration
- **Puzzle**: Complete word puzzle system with letter revelation
- **Game**: Full game state management and turn-based logic
- **Round**: Individual round tracking with puzzle completion

### Game Engine
- **GameEngine**: High-level API for all game operations
- **PuzzleManager**: JSON-based puzzle loading and management
- **ScoreManager**: Comprehensive scoring and leaderboard system

### Key Features
- **Manual Wheel Input**: Designed for physical wheel use
- **Rich Game State**: Comprehensive status information for UI
- **Event-Driven**: All actions return detailed result objects
- **Zero Dependencies**: Pure Python standard library implementation

## Quick Start (Backend Demo)

```bash
cd backend
python3 tests/test_basic.py  # Run tests
python3 main.py demo         # See demo
python3 main.py              # Interactive mode
```

## Game Rules

"Wheel of Fortune" combines word puzzles with chance:

1. **Teams take turns** spinning a wheel and guessing letters
2. **Money segments** award cash for correct consonant guesses
3. **Special segments** create gameplay variety (BANKRUPT, FREE SPIN, etc.)
4. **Vowels cost $250** but don't earn money
5. **Solve the puzzle** to win the round and keep your money
6. **Highest total** after all rounds wins the game

## Architecture

```
wheel_of_fortune/
├── backend/              # ✅ Complete Python backend
│   ├── models/          # Game data models
│   ├── managers/        # Business logic
│   ├── utils/           # Utilities and constants
│   ├── data/            # Puzzle data files
│   ├── tests/           # Unit tests
│   └── main.py          # CLI demo
└── frontend/            # 🚧 Planned frontend
```

## Frontend Development Plan

The backend provides a clean API ready for any frontend technology:

### Recommended Tech Stack Options
1. **Web App**: React/Vue.js + Python Flask/FastAPI
2. **Desktop**: Electron or Python Tkinter/PyQt
3. **Mobile**: React Native or Flutter with API backend

### Key Integration Points
- **GameEngine**: Single interface for all game operations
- **WheelResult Enum**: Easy dropdown/button wheel selection
- **Rich State Objects**: Complete game status for UI updates
- **Event Responses**: Detailed action results for user feedback

### UI Components Needed
- **Team Setup**: Create teams and add members
- **Game Board**: Display puzzle, category, and guessed letters
- **Wheel Interface**: Select wheel result from enum options
- **Action Buttons**: Guess letter, buy vowel, solve puzzle
- **Scoreboard**: Show team money and leaderboard
- **Game Controls**: Round progression and game management

## Design Philosophy

- **Physical Integration**: Complement real-world wheel spinning
- **Team-Oriented**: Built for group play and social interaction
- **Flexible Configuration**: Adaptable to different group sizes
- **Simple Deployment**: Minimal dependencies for easy setup
- **Extensible**: Easy to add puzzles, modify rules, or enhance features

## Next Steps

1. **Choose Frontend Technology** based on your preferences
2. **Create UI Mockups** for the game interface
3. **Set up API Layer** (Flask/FastAPI) if building web app
4. **Implement Core Components** using the backend GameEngine
5. **Add Polish**: Animations, sounds, and enhanced user experience

The backend foundation is solid and ready for any frontend approach!

## Development Notes

- **Python 3.8+** required for backend
- **No external dependencies** for core game logic
- **JSON-based puzzle storage** for easy customization
- **Comprehensive error handling** and validation
- **Full test coverage** of core functionality
- **Type hints throughout** for better code quality

Ready to build an amazing Wheel of Fortune experience! 🎡
