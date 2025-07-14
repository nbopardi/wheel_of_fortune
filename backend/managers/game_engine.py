from typing import List, Dict, Optional
from models.game import Game, GameState, TurnState
from models.team import Team
from models.round import Round
from models.wheel_result import WheelResult
from utils.constants import DEFAULT_TOTAL_ROUNDS, VOWEL_COST
from .puzzle_manager import PuzzleManager
from .score_manager import ScoreManager


class GameEngine:
    """High-level game engine that orchestrates Wheel of Fortune gameplay."""
    
    def __init__(self, data_dir: str = "backend/data"):
        """
        Initialize the game engine.
        
        Args:
            data_dir: Directory containing game data files
        """
        self.puzzle_manager = PuzzleManager(data_dir)
        self.current_game: Optional[Game] = None
        self.score_manager: Optional[ScoreManager] = None
    
    def create_game(self, team_data: List[Dict], total_rounds: int = DEFAULT_TOTAL_ROUNDS) -> Dict:
        """
        Create a new game with the specified teams.
        
        Args:
            team_data: List of team dictionaries with 'name' and 'members' keys
            total_rounds: Number of rounds to play
            
        Returns:
            Dict: Game creation result with game info
        """
        try:
            # Create teams
            teams = []
            for team_info in team_data:
                team = Team(name=team_info["name"], members=team_info["members"])
                teams.append(team)
            
            # Create game
            self.current_game = Game(teams=teams, total_rounds=total_rounds)
            
            # Create rounds with random puzzles
            for round_num in range(1, total_rounds + 1):
                puzzle = self.puzzle_manager.get_random_puzzle()
                round_obj = Round(puzzle=puzzle, round_number=round_num)
                self.current_game.add_round(round_obj)
            
            # Initialize score manager
            self.score_manager = ScoreManager(self.current_game)
            
            return {
                "success": True,
                "game_id": self.current_game.game_id,
                "message": f"Game created with {len(teams)} teams and {total_rounds} rounds",
                "game_status": self.current_game.get_game_status()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create game"
            }
    
    def start_game(self) -> Dict:
        """
        Start the current game.
        
        Returns:
            Dict: Game start result
        """
        if not self.current_game:
            return {
                "success": False,
                "error": "No game to start",
                "message": "Create a game first"
            }
        
        try:
            self.current_game.start_game()
            return {
                "success": True,
                "message": "Game started successfully",
                "game_status": self.current_game.get_game_status(),
                "current_team": self.current_game.get_current_team().name,
                "current_puzzle": {
                    "category": self.current_game.get_current_round().get_category(),
                    "display": self.current_game.get_current_round().get_puzzle_display()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to start game"
            }
    
    def process_wheel_spin(self, wheel_result: WheelResult) -> Dict:
        """
        Process a manual wheel spin result.
        
        Args:
            wheel_result: The result from the physical wheel
            
        Returns:
            Dict: Wheel spin processing result
        """
        if not self.current_game:
            return self._no_game_error()
        
        try:
            result = self.current_game.input_wheel_result(wheel_result)
            
            response = {
                "success": True,
                "wheel_result": wheel_result.value,
                "team": result["team"],
                "message": result["message"],
                "turn_continues": result["turn_continues"],
                "action_required": result.get("action_required"),
                "game_status": self.current_game.get_game_status()
            }
            
            # Add scoring information if available
            if self.score_manager:
                response["leaderboard"] = self.score_manager.get_leaderboard()
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process wheel spin"
            }
    
    def process_letter_guess(self, letter: str) -> Dict:
        """
        Process a letter guess from the current team.
        
        Args:
            letter: The letter being guessed
            
        Returns:
            Dict: Letter guess processing result
        """
        if not self.current_game:
            return self._no_game_error()
        
        try:
            result = self.current_game.guess_letter(letter)
            
            response = {
                "success": True,
                "letter": result["letter"],
                "in_puzzle": result["in_puzzle"],
                "team": result["team"],
                "money_earned": result["money_earned"],
                "turn_continues": result["turn_continues"],
                "puzzle_solved": result["puzzle_solved"],
                "game_status": self.current_game.get_game_status()
            }
            
            if result["puzzle_solved"]:
                response["message"] = f"Congratulations! {result['team']} solved the puzzle!"
                response["solution"] = self.current_game.get_current_round().get_solution()
            elif result["in_puzzle"]:
                response["message"] = f"Good guess! '{letter}' appears {self.current_game.get_current_round().puzzle.count_letter_occurrences(letter)} time(s)"
            else:
                response["message"] = f"Sorry, '{letter}' is not in the puzzle"
            
            # Add scoring information
            if self.score_manager:
                response["leaderboard"] = self.score_manager.get_leaderboard()
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process letter guess"
            }
    
    def process_vowel_purchase(self, vowel: str) -> Dict:
        """
        Process a vowel purchase from the current team.
        
        Args:
            vowel: The vowel to purchase
            
        Returns:
            Dict: Vowel purchase processing result
        """
        if not self.current_game:
            return self._no_game_error()
        
        try:
            result = self.current_game.buy_vowel(vowel)
            
            response = {
                "success": True,
                "vowel": result["vowel"],
                "cost": result["cost"],
                "in_puzzle": result["in_puzzle"],
                "team": result["team"],
                "puzzle_solved": result["puzzle_solved"],
                "game_status": self.current_game.get_game_status()
            }
            
            if result["puzzle_solved"]:
                response["message"] = f"Congratulations! {result['team']} solved the puzzle!"
                response["solution"] = self.current_game.get_current_round().get_solution()
            elif result["in_puzzle"]:
                response["message"] = f"Good purchase! '{vowel}' is in the puzzle"
            else:
                response["message"] = f"'{vowel}' is not in the puzzle"
            
            # Add scoring information
            if self.score_manager:
                response["leaderboard"] = self.score_manager.get_leaderboard()
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process vowel purchase"
            }
    
    def process_solve_attempt(self, solution_guess: str) -> Dict:
        """
        Process a solve attempt from the current team.
        
        Args:
            solution_guess: The team's guess for the complete solution
            
        Returns:
            Dict: Solve attempt processing result
        """
        if not self.current_game:
            return self._no_game_error()
        
        try:
            result = self.current_game.attempt_solve(solution_guess)
            
            response = {
                "success": True,
                "guess": result["guess"],
                "correct": result["correct"],
                "team": result["team"],
                "solution": result["solution"],
                "game_status": self.current_game.get_game_status()
            }
            
            if result["correct"]:
                response["message"] = f"Congratulations! {result['team']} solved the puzzle correctly!"
            else:
                response["message"] = f"Sorry, that's not correct. The solution was: {result['solution']}"
            
            # Add scoring information
            if self.score_manager:
                response["leaderboard"] = self.score_manager.get_leaderboard()
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process solve attempt"
            }
    
    def continue_to_next_round(self) -> Dict:
        """
        Continue from a completed round to the next round.
        
        Returns:
            Dict: Next round continuation result
        """
        if not self.current_game:
            return self._no_game_error()
        
        try:
            self.current_game.continue_to_next_round()
            
            return {
                "success": True,
                "message": f"Continuing to Round {self.current_game.current_round_index + 1}",
                "game_status": self.current_game.get_game_status(),
                "current_puzzle": {
                    "category": self.current_game.get_current_round().get_category(),
                    "display": self.current_game.get_current_round().get_puzzle_display()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to continue to next round"
            }
    
    def get_game_status(self) -> Dict:
        """
        Get the current game status.
        
        Returns:
            Dict: Current game status
        """
        if not self.current_game:
            return {
                "success": False,
                "message": "No active game",
                "game_status": None
            }
        
        return {
            "success": True,
            "game_status": self.current_game.get_game_status()
        }
    
    def get_available_wheel_options(self) -> Dict:
        """
        Get all available wheel result options.
        
        Returns:
            Dict: Available wheel options categorized
        """
        return {
            "money_options": [{"name": result.name, "value": result.value} 
                            for result in WheelResult.get_all_money_options()],
            "special_options": [{"name": result.name, "value": result.value} 
                              for result in WheelResult.get_all_special_options()],
            "all_options": [{"name": result.name, "value": result.value} 
                          for result in WheelResult]
        }
    
    def get_game_summary(self) -> Dict:
        """
        Get a comprehensive game summary.
        
        Returns:
            Dict: Complete game summary
        """
        if not self.current_game or not self.score_manager:
            return self._no_game_error()
        
        return {
            "success": True,
            "game_summary": self.score_manager.get_game_summary(),
            "leaderboard": self.score_manager.get_leaderboard(),
            "puzzle_info": {
                "total_puzzles": self.puzzle_manager.get_puzzle_count(),
                "categories": self.puzzle_manager.get_all_categories()
            }
        }
    
    def _no_game_error(self) -> Dict:
        """Standard response for when no game is active."""
        return {
            "success": False,
            "error": "No active game",
            "message": "Create and start a game first"
        } 