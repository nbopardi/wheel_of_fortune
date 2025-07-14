#!/usr/bin/env python3
"""
Wheel of Fortune - Backend Demo
A command-line demonstration of the Wheel of Fortune game engine.
"""

import sys
import os
from typing import List, Dict

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from managers.game_engine import GameEngine
from models.wheel_result import WheelResult


def display_banner():
    """Display the game banner."""
    print("=" * 60)
    print("🎡 WHEEL OF FORTUNE - BACKEND DEMO 🎡")
    print("=" * 60)
    print()


def create_sample_teams() -> List[Dict]:
    """Create sample teams for demonstration."""
    return [
        {"name": "Team Alpha", "members": ["Alice", "Bob"]},
        {"name": "Team Beta", "members": ["Charlie", "Diana"]},
        {"name": "Team Gamma", "members": ["Eve", "Frank"]}
    ]


def display_wheel_options():
    """Display available wheel options."""
    print("\n📍 Available Wheel Options:")
    print("Money Values:")
    for result in WheelResult.get_all_money_options():
        print(f"  - {result.name}: ${result.value}")
    
    print("\nSpecial Segments:")
    for result in WheelResult.get_all_special_options():
        print(f"  - {result.name}")
    print()


def display_game_status(game_engine: GameEngine):
    """Display current game status."""
    status_result = game_engine.get_game_status()
    if not status_result["success"]:
        print(f"❌ {status_result['message']}")
        return
    
    status = status_result["game_status"]
    print(f"\n🎮 Game Status:")
    print(f"   Game ID: {status['game_id']}")
    print(f"   State: {status['game_state']}")
    print(f"   Round: {status['current_round']}/{status['total_rounds']}")
    
    if "current_puzzle" in status:
        puzzle = status["current_puzzle"]
        print(f"\n🧩 Current Puzzle:")
        print(f"   Category: {puzzle['category']}")
        print(f"   Display: {puzzle['display']}")
        print(f"   Guessed Letters: {', '.join(sorted(puzzle['guessed_letters'])) if puzzle['guessed_letters'] else 'None'}")
    
    print(f"\n👥 Teams:")
    for team in status["teams"]:
        indicator = "👉" if team["is_current_turn"] else "  "
        print(f"   {indicator} {team['name']} (${team['current_round_money']} / Total: ${team['total_money']})")
        print(f"      Members: {', '.join(team['members'])}")
    print()


def demo_game_creation():
    """Demonstrate game creation and basic functionality."""
    display_banner()
    
    # Initialize game engine
    print("🔧 Initializing Game Engine...")
    game_engine = GameEngine()
    
    # Create teams
    print("👥 Creating teams...")
    teams = create_sample_teams()
    
    # Create game
    print("🎮 Creating game...")
    result = game_engine.create_game(teams, total_rounds=2)  # Shorter demo
    
    if not result["success"]:
        print(f"❌ Failed to create game: {result['message']}")
        return
    
    print(f"✅ {result['message']}")
    
    # Start game
    print("🚀 Starting game...")
    result = game_engine.start_game()
    
    if not result["success"]:
        print(f"❌ Failed to start game: {result['message']}")
        return
    
    print(f"✅ {result['message']}")
    
    # Display initial status
    display_game_status(game_engine)
    
    # Show wheel options
    display_wheel_options()
    
    # Demonstrate a few game actions
    print("🎯 Demonstrating game actions...")
    
    # Spin 1: Money value
    print("\n1️⃣ Team Alpha spins the wheel and gets $500...")
    result = game_engine.process_wheel_spin(WheelResult.MONEY_500)
    print(f"   Result: {result['message']}")
    
    if result["success"] and result.get("action_required") == "guess_consonant":
        # Guess a consonant
        print("   Team Alpha guesses 'T'...")
        letter_result = game_engine.process_letter_guess("T")
        print(f"   Result: {letter_result['message']}")
        
        if letter_result["success"] and letter_result["in_puzzle"]:
            print(f"   Money earned: ${letter_result['money_earned']}")
    
    # Display updated status
    display_game_status(game_engine)
    
    # Spin 2: Special segment
    print("2️⃣ Team Beta spins the wheel and gets BANKRUPT...")
    result = game_engine.process_wheel_spin(WheelResult.BANKRUPT)
    print(f"   Result: {result['message']}")
    
    # Display final status
    display_game_status(game_engine)
    
    # Show game summary
    summary_result = game_engine.get_game_summary()
    if summary_result["success"]:
        summary = summary_result["game_summary"]
        print(f"📊 Game Summary:")
        print(f"   Total money in play: ${summary['total_money_in_play']}")
        print(f"   Completed rounds: {summary['completed_rounds']}")
        if summary["leader"]:
            print(f"   Current leader: {summary['leader']['team_name']} (${summary['leader']['total_money']})")
    
    print("\n🎉 Demo completed! The backend is working correctly.")
    print("📝 Next step: Create the frontend interface.")


def interactive_mode():
    """Run an interactive mode for testing."""
    display_banner()
    print("🔄 Interactive Mode - Type 'help' for commands")
    
    game_engine = GameEngine()
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif command == 'help':
                print("Available commands:")
                print("  create - Create a new game")
                print("  start - Start the game")
                print("  status - Show game status")
                print("  wheels - Show wheel options")
                print("  demo - Run automatic demo")
                print("  quit - Exit")
            elif command == 'create':
                teams = create_sample_teams()
                result = game_engine.create_game(teams)
                print(f"Result: {result['message']}")
            elif command == 'start':
                result = game_engine.start_game()
                print(f"Result: {result['message']}")
            elif command == 'status':
                display_game_status(game_engine)
            elif command == 'wheels':
                display_wheel_options()
            elif command == 'demo':
                demo_game_creation()
                break
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_game_creation()
    else:
        interactive_mode() 