from typing import List, Optional, Dict
from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum

from models.team import Team
from models.round import Round
from models.wheel_result import WheelResult


class GameState(Enum):
    """Enum representing the current state of the game."""
    SETUP = "SETUP"
    IN_PROGRESS = "IN_PROGRESS"
    ROUND_COMPLETED = "ROUND_COMPLETED"
    GAME_COMPLETED = "GAME_COMPLETED"


class TurnState(Enum):
    """Enum representing the current state of a team's turn."""
    WAITING_FOR_SPIN = "WAITING_FOR_SPIN"
    WAITING_FOR_LETTER_GUESS = "WAITING_FOR_LETTER_GUESS"
    WAITING_FOR_SOLVE_ATTEMPT = "WAITING_FOR_SOLVE_ATTEMPT"
    TURN_ENDED = "TURN_ENDED"


@dataclass
class Game:
    """Main game controller for Wheel of Fortune."""
    
    teams: List[Team]
    rounds: List[Round] = field(default_factory=list)
    current_round_index: int = 0
    current_team_index: int = 0
    game_state: GameState = GameState.SETUP
    turn_state: TurnState = TurnState.WAITING_FOR_SPIN
    total_rounds: int = 3
    vowel_cost: int = 250
    game_id: str = field(default_factory=lambda: str(uuid4()))
    last_wheel_result: Optional[WheelResult] = None
    
    def __post_init__(self):
        """Validate game data after initialization."""
        if len(self.teams) < 2:
            raise ValueError("Game must have at least 2 teams")
        if len(self.teams) > 6:
            raise ValueError("Game cannot have more than 6 teams")
        if self.total_rounds < 1:
            raise ValueError("Game must have at least 1 round")
    
    def start_game(self) -> None:
        """Start the game - must have rounds added first."""
        if len(self.rounds) != self.total_rounds:
            raise ValueError(f"Game must have exactly {self.total_rounds} rounds to start")
        
        self.game_state = GameState.IN_PROGRESS
        self.turn_state = TurnState.WAITING_FOR_SPIN
        self.current_round_index = 0
        self.current_team_index = 0
    
    def add_round(self, round_obj: Round) -> None:
        """Add a round to the game."""
        if self.game_state != GameState.SETUP:
            raise ValueError("Cannot add rounds after game has started")
        
        if len(self.rounds) >= self.total_rounds:
            raise ValueError(f"Game already has maximum {self.total_rounds} rounds")
        
        self.rounds.append(round_obj)
    
    def get_current_team(self) -> Team:
        """Get the team whose turn it currently is."""
        if self.game_state == GameState.SETUP:
            raise ValueError("Game has not started yet")
        return self.teams[self.current_team_index]
    
    def get_current_round(self) -> Round:
        """Get the current round being played."""
        if self.game_state == GameState.SETUP:
            raise ValueError("Game has not started yet")
        return self.rounds[self.current_round_index]
    
    def input_wheel_result(self, wheel_result: WheelResult) -> Dict:
        """
        Input the result of a physical wheel spin.
        
        Args:
            wheel_result: The result from the physical wheel
            
        Returns:
            dict: Information about what happened and what to do next
        """
        if self.turn_state != TurnState.WAITING_FOR_SPIN:
            raise ValueError(f"Not waiting for wheel spin. Current state: {self.turn_state}")
        
        self.last_wheel_result = wheel_result
        current_team = self.get_current_team()
        
        result_info = {
            "wheel_result": wheel_result,
            "team": current_team.name,
            "action_required": None,
            "turn_continues": True,
            "message": ""
        }
        
        if wheel_result.is_money():
            # Money segment - team can guess a consonant
            self.turn_state = TurnState.WAITING_FOR_LETTER_GUESS
            result_info["action_required"] = "guess_consonant"
            result_info["message"] = f"{current_team.name} spun ${wheel_result.get_money_value()}! Guess a consonant."
            
        elif wheel_result == WheelResult.BANKRUPT:
            # Lose all round money and end turn
            current_team.lose_round_money()
            self._end_turn()
            result_info["turn_continues"] = False
            result_info["message"] = f"{current_team.name} hit BANKRUPT! Lost all round money. Turn ends."
            
        elif wheel_result == WheelResult.LOSE_A_TURN:
            # Just end the turn
            self._end_turn()
            result_info["turn_continues"] = False
            result_info["message"] = f"{current_team.name} lost their turn!"
            
        elif wheel_result == WheelResult.FREE_SPIN:
            # Give free spin and continue turn
            current_team.give_free_spin()
            self.turn_state = TurnState.WAITING_FOR_SPIN
            result_info["action_required"] = "spin_again"
            result_info["message"] = f"{current_team.name} earned a FREE SPIN! Spin again."
            
        return result_info
    
    def guess_letter(self, letter: str) -> Dict:
        """
        Process a letter guess from the current team.
        
        Args:
            letter: The letter being guessed
            
        Returns:
            dict: Information about the guess result
        """
        if self.turn_state != TurnState.WAITING_FOR_LETTER_GUESS:
            raise ValueError(f"Not waiting for letter guess. Current state: {self.turn_state}")
        
        if not self.last_wheel_result or not self.last_wheel_result.is_money():
            raise ValueError("No valid money wheel result for this guess")
        
        current_team = self.get_current_team()
        current_round = self.get_current_round()
        puzzle = current_round.puzzle
        
        # Check if letter is a consonant
        if not puzzle.is_consonant(letter):
            raise ValueError("Can only guess consonants after spinning money")
        
        # Make the guess
        letter_in_puzzle = puzzle.guess_letter(letter)
        
        result_info = {
            "letter": letter.upper(),
            "in_puzzle": letter_in_puzzle,
            "team": current_team.name,
            "money_earned": 0,
            "turn_continues": letter_in_puzzle,
            "puzzle_solved": False
        }
        
        if letter_in_puzzle:
            # Calculate money earned
            occurrences = puzzle.count_letter_occurrences(letter)
            money_earned = occurrences * self.last_wheel_result.get_money_value()
            current_team.add_money(money_earned)
            result_info["money_earned"] = money_earned
            
            # Check if puzzle is now solved
            if puzzle.is_solved():
                self._complete_current_round()
                result_info["puzzle_solved"] = True
                result_info["turn_continues"] = False
            else:
                # Team can continue (spin again or solve)
                self.turn_state = TurnState.WAITING_FOR_SPIN
        else:
            # Wrong guess - end turn
            self._end_turn()
        
        return result_info
    
    def buy_vowel(self, vowel: str) -> Dict:
        """
        Allow current team to buy a vowel.
        
        Args:
            vowel: The vowel to buy
            
        Returns:
            dict: Information about the vowel purchase
        """
        current_team = self.get_current_team()
        current_round = self.get_current_round()
        puzzle = current_round.puzzle
        
        # Validate vowel purchase
        if not puzzle.is_vowel(vowel):
            raise ValueError(f"'{vowel}' is not a vowel")
        
        if not current_team.can_buy_vowel(self.vowel_cost):
            raise ValueError(f"Team doesn't have enough money to buy vowel (${self.vowel_cost})")
        
        # Buy the vowel
        current_team.buy_vowel(self.vowel_cost)
        vowel_in_puzzle = puzzle.guess_letter(vowel)
        
        result_info = {
            "vowel": vowel.upper(),
            "cost": self.vowel_cost,
            "in_puzzle": vowel_in_puzzle,
            "team": current_team.name,
            "puzzle_solved": False
        }
        
        # Check if puzzle is solved
        if puzzle.is_solved():
            self._complete_current_round()
            result_info["puzzle_solved"] = True
        
        return result_info
    
    def attempt_solve(self, solution_guess: str) -> Dict:
        """
        Allow current team to attempt to solve the puzzle.
        
        Args:
            solution_guess: The team's guess for the complete solution
            
        Returns:
            dict: Information about the solve attempt
        """
        current_team = self.get_current_team()
        current_round = self.get_current_round()
        puzzle = current_round.puzzle
        
        is_correct = puzzle.attempt_solve(solution_guess)
        
        result_info = {
            "guess": solution_guess,
            "correct": is_correct,
            "team": current_team.name,
            "solution": puzzle.solution
        }
        
        if is_correct:
            self._complete_current_round()
        else:
            self._end_turn()
        
        return result_info
    
    def _complete_current_round(self) -> None:
        """Complete the current round and advance to next round or end game."""
        current_team = self.get_current_team()
        current_round = self.get_current_round()
        
        # Complete the round
        current_round.complete_round(current_team)
        
        # Check if this was the last round
        if self.current_round_index >= len(self.rounds) - 1:
            self.game_state = GameState.GAME_COMPLETED
        else:
            self.current_round_index += 1
            self.game_state = GameState.ROUND_COMPLETED
            self.turn_state = TurnState.WAITING_FOR_SPIN
            self.current_team_index = 0  # Start next round with first team
    
    def _end_turn(self) -> None:
        """End the current team's turn and move to next team."""
        self.turn_state = TurnState.TURN_ENDED
        self._advance_to_next_team()
    
    def _advance_to_next_team(self) -> None:
        """Move to the next team's turn."""
        self.current_team_index = (self.current_team_index + 1) % len(self.teams)
        self.turn_state = TurnState.WAITING_FOR_SPIN
        self.last_wheel_result = None
    
    def continue_to_next_round(self) -> None:
        """Continue from round completed state to next round."""
        if self.game_state != GameState.ROUND_COMPLETED:
            raise ValueError("Game is not in round completed state")
        
        self.game_state = GameState.IN_PROGRESS
        
        # Reset all teams' round money for the new round
        for team in self.teams:
            team.current_round_money = 0
    
    def get_game_status(self) -> Dict:
        """Get comprehensive game status information."""
        status = {
            "game_id": self.game_id,
            "game_state": self.game_state.value,
            "turn_state": self.turn_state.value,
            "current_round": self.current_round_index + 1,
            "total_rounds": self.total_rounds,
            "teams": [
                {
                    "name": team.name,
                    "members": team.members,
                    "current_round_money": team.current_round_money,
                    "total_money": team.total_money,
                    "has_free_spin": team.has_free_spin,
                    "is_current_turn": i == self.current_team_index
                }
                for i, team in enumerate(self.teams)
            ]
        }
        
        if self.game_state != GameState.SETUP:
            current_round = self.get_current_round()
            status["current_puzzle"] = {
                "category": current_round.get_category(),
                "display": current_round.get_puzzle_display(),
                "guessed_letters": list(current_round.puzzle.guessed_letters),
                "available_consonants": list(current_round.puzzle.get_available_consonants()),
                "available_vowels": list(current_round.puzzle.get_available_vowels())
            }
        
        if self.last_wheel_result:
            status["last_wheel_result"] = self.last_wheel_result.value
        
        return status
    
    def get_winner(self) -> Optional[Team]:
        """Get the winning team (only valid when game is completed)."""
        if self.game_state != GameState.GAME_COMPLETED:
            return None
        
        return max(self.teams, key=lambda team: team.total_money)
    
    def __str__(self) -> str:
        return f"Game {self.game_id}: Round {self.current_round_index + 1}/{self.total_rounds} - {self.game_state.value}" 