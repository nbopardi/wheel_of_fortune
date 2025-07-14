"""
Basic tests for Wheel of Fortune backend functionality.
"""

import sys
import os

# Add backend directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.wheel_result import WheelResult
from models.team import Team
from models.puzzle import Puzzle
from models.round import Round
from models.game import Game, GameState


def test_wheel_result_enum():
    """Test WheelResult enum functionality."""
    print("Testing WheelResult enum...")
    
    # Test money values
    assert WheelResult.MONEY_500.is_money()
    assert WheelResult.MONEY_500.get_money_value() == 500
    assert not WheelResult.BANKRUPT.is_money()
    
    # Test special segments
    assert WheelResult.BANKRUPT.is_special()
    assert not WheelResult.MONEY_500.is_special()
    
    # Test class methods
    money_options = WheelResult.get_all_money_options()
    assert len(money_options) > 0
    assert all(option.is_money() for option in money_options)
    
    print("✅ WheelResult enum tests passed")


def test_team_model():
    """Test Team model functionality."""
    print("Testing Team model...")
    
    # Create team
    team = Team(name="Test Team", members=["Alice", "Bob"])
    assert team.name == "Test Team"
    assert len(team.members) == 2
    assert team.current_round_money == 0
    assert team.total_money == 0
    
    # Test money operations
    team.add_money(500)
    assert team.current_round_money == 500
    
    team.win_round()
    assert team.total_money == 500
    assert team.current_round_money == 0
    
    # Test vowel purchase
    team.add_money(300)
    assert team.can_buy_vowel(250)
    team.buy_vowel(250)
    assert team.current_round_money == 50
    
    print("✅ Team model tests passed")


def test_puzzle_model():
    """Test Puzzle model functionality."""
    print("Testing Puzzle model...")
    
    puzzle = Puzzle(solution="HELLO WORLD", category="PHRASE")
    assert puzzle.solution == "HELLO WORLD"
    assert puzzle.category == "PHRASE"
    
    # Test letter guessing
    display = puzzle.get_display()
    assert display == "_____ _____"
    
    # Guess a letter
    result = puzzle.guess_letter("L")
    assert result == True  # L is in HELLO WORLD
    assert puzzle.count_letter_occurrences("L") == 3
    
    # Test display with guessed letter
    display = puzzle.get_display()
    assert "L" in display
    
    # Test solve attempt
    assert puzzle.attempt_solve("HELLO WORLD") == True
    assert puzzle.attempt_solve("WRONG GUESS") == False
    
    print("✅ Puzzle model tests passed")


def test_game_creation():
    """Test basic game creation and flow."""
    print("Testing Game creation...")
    
    # Create teams
    teams = [
        Team(name="Team A", members=["Alice"]),
        Team(name="Team B", members=["Bob"])
    ]
    
    # Create game
    game = Game(teams=teams, total_rounds=1)
    assert game.game_state == GameState.SETUP
    assert len(game.teams) == 2
    
    # Add a round
    puzzle = Puzzle(solution="TEST", category="PHRASE")
    round_obj = Round(puzzle=puzzle, round_number=1)
    game.add_round(round_obj)
    
    # Start game
    game.start_game()
    assert game.game_state == GameState.IN_PROGRESS
    
    # Test wheel input
    result = game.input_wheel_result(WheelResult.MONEY_500)
    assert result["wheel_result"] == WheelResult.MONEY_500
    
    print("✅ Game creation tests passed")


def run_all_tests():
    """Run all basic tests."""
    print("🧪 Running basic backend tests...")
    print()
    
    try:
        test_wheel_result_enum()
        test_team_model()
        test_puzzle_model()
        test_game_creation()
        
        print()
        print("🎉 All basic tests passed!")
        print("✅ Backend implementation is working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 