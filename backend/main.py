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


def create_custom_teams() -> List[Dict]:
    """Interactive team creation."""
    teams = []
    
    while True:
        try:
            num_teams = int(input("How many teams? (2-6): "))
            if 2 <= num_teams <= 6:
                break
            else:
                print("Please enter a number between 2 and 6.")
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nCreating {num_teams} teams...")
    
    for i in range(num_teams):
        print(f"\n--- Team {i + 1} ---")
        
        while True:
            team_name = input(f"Enter team {i + 1} name: ").strip()
            if team_name:
                break
            print("Team name cannot be empty.")
        
        members = []
        while True:
            try:
                num_members = int(input(f"How many members in {team_name}? (1-6): "))
                if 1 <= num_members <= 6:
                    break
                else:
                    print("Please enter a number between 1 and 6.")
            except ValueError:
                print("Please enter a valid number.")
        
        for j in range(num_members):
            while True:
                member_name = input(f"  Member {j + 1} name: ").strip()
                if member_name:
                    members.append(member_name)
                    break
                print("Member name cannot be empty.")
        
        teams.append({"name": team_name, "members": members})
        print(f"✅ {team_name} created with {len(members)} members: {', '.join(members)}")
    
    return teams


def display_wheel_options():
    """Display available wheel options."""
    print("\n📍 Available Wheel Options:")
    print("Money Values:")
    money_options = WheelResult.get_all_money_options()
    for i, result in enumerate(money_options, 1):
        print(f"  {i:2d}. {result.name}: ${result.value}")
    
    print("\nSpecial Segments:")
    special_options = WheelResult.get_all_special_options()
    for i, result in enumerate(special_options, len(money_options) + 1):
        print(f"  {i:2d}. {result.name}")
    print()


def get_wheel_result_input() -> WheelResult:
    """Get wheel result from user input."""
    while True:
        print("\n🎯 Enter the result of your physical wheel spin:")
        display_wheel_options()
        
        try:
            choice = int(input("Enter option number: "))
            all_options = list(WheelResult)
            
            if 1 <= choice <= len(all_options):
                selected_result = all_options[choice - 1]
                print(f"Selected: {selected_result.name} ({selected_result.value})")
                
                confirm = input("Is this correct? (y/n): ").lower().strip()
                if confirm in ['y', 'yes']:
                    return selected_result
            else:
                print(f"Please enter a number between 1 and {len(all_options)}.")
                
        except ValueError:
            print("Please enter a valid number.")


def get_letter_input(available_letters: List[str], letter_type: str = "consonant") -> str:
    """Get a letter input from user."""
    while True:
        print(f"\nAvailable {letter_type}s: {', '.join(sorted(available_letters))}")
        letter = input(f"Enter a {letter_type}: ").strip().upper()
        
        if len(letter) == 1 and letter.isalpha() and letter in available_letters:
            return letter
        elif letter not in available_letters:
            print(f"'{letter}' has already been guessed or is not a valid {letter_type}.")
        else:
            print("Please enter a single letter.")


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
        if team["has_free_spin"]:
            print(f"      🎁 Has FREE SPIN!")
    print()


def play_interactive_game():
    """Play an interactive game with user input."""
    display_banner()
    print("🎮 Starting Interactive Wheel of Fortune Game!")
    
    # Initialize game engine
    game_engine = GameEngine()
    
    # Create teams
    teams = create_custom_teams()
    
    # Get number of rounds
    while True:
        try:
            total_rounds = int(input(f"\nHow many rounds? (1-5): "))
            if 1 <= total_rounds <= 5:
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Create and start game
    print(f"\n🎮 Creating game with {len(teams)} teams and {total_rounds} rounds...")
    result = game_engine.create_game(teams, total_rounds=total_rounds)
    
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
    
    # Main game loop
    while True:
        display_game_status(game_engine)
        
        status = game_engine.get_game_status()
        if not status["success"]:
            break
            
        game_status = status["game_status"]
        
        # Check if game is completed
        if game_status["game_state"] == "GAME_COMPLETED":
            print("🎉 Game completed!")
            summary_result = game_engine.get_game_summary()
            if summary_result["success"]:
                leaderboard = summary_result["leaderboard"]
                print("\n🏆 Final Results:")
                for i, team in enumerate(leaderboard):
                    trophy = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
                    print(f"   {trophy} {team['position']}. {team['team_name']}: ${team['total_money']}")
            break
        
        # Check if round is completed
        if game_status["game_state"] == "ROUND_COMPLETED":
            print("🎯 Round completed!")
            continue_game = input("Continue to next round? (y/n): ").lower().strip()
            if continue_game in ['y', 'yes']:
                game_engine.continue_to_next_round()
                continue
            else:
                break
        
        # Current team's turn
        current_team = None
        for team in game_status["teams"]:
            if team["is_current_turn"]:
                current_team = team
                break
        
        if not current_team:
            print("❌ No current team found")
            break
        
        print(f"\n🎯 {current_team['name']}'s turn!")
        
        # Show available actions
        turn_state = game_status["turn_state"]
        
        if turn_state == "WAITING_FOR_SPIN":
            print("1. Spin the wheel")
            print("2. Buy a vowel ($250)")
            print("3. Solve the puzzle")
            print("4. Show game status")
            print("5. Quit game")
            
            choice = input("Choose an action (1-5): ").strip()
            
            if choice == "1":
                # Spin wheel
                wheel_result = get_wheel_result_input()
                result = game_engine.process_wheel_spin(wheel_result)
                print(f"\n{result['message']}")
                
            elif choice == "2":
                # Buy vowel
                puzzle = game_status["current_puzzle"]
                available_vowels = puzzle["available_vowels"]
                
                if not available_vowels:
                    print("No vowels available to buy!")
                    continue
                    
                if current_team["current_round_money"] < 250:
                    print(f"Not enough money! Need $250, have ${current_team['current_round_money']}")
                    continue
                
                vowel = get_letter_input(available_vowels, "vowel")
                result = game_engine.process_vowel_purchase(vowel)
                print(f"\n{result['message']}")
                
            elif choice == "3":
                # Solve puzzle
                solution = input("Enter your solution: ").strip()
                if solution:
                    result = game_engine.process_solve_attempt(solution)
                    print(f"\n{result['message']}")
                    
            elif choice == "4":
                # Show status (will be shown at start of next loop)
                continue
                
            elif choice == "5":
                # Quit
                print("👋 Thanks for playing!")
                break
                
            else:
                print("Invalid choice. Please try again.")
                
        elif turn_state == "WAITING_FOR_LETTER_GUESS":
            puzzle = game_status["current_puzzle"]
            available_consonants = puzzle["available_consonants"]
            
            if not available_consonants:
                print("No consonants available!")
                continue
            
            consonant = get_letter_input(available_consonants, "consonant")
            result = game_engine.process_letter_guess(consonant)
            print(f"\n{result['message']}")
            
            if "money_earned" in result and result["money_earned"] > 0:
                print(f"💰 Earned: ${result['money_earned']}")
        
        else:
            print(f"Unexpected turn state: {turn_state}")
            break


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
                print("  play - Start an interactive game")
                print("  create - Create a new game with sample teams")
                print("  start - Start the game")
                print("  status - Show game status")
                print("  wheels - Show wheel options")
                print("  demo - Run automatic demo")
                print("  quit - Exit")
            elif command == 'play':
                play_interactive_game()
                break
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
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            demo_game_creation()
        elif sys.argv[1] == "play":
            play_interactive_game()
        else:
            print("Usage: python3 main.py [demo|play]")
    else:
        interactive_mode() 