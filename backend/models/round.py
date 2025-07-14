from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass
from uuid import uuid4

from models.puzzle import Puzzle

if TYPE_CHECKING:
    from models.team import Team


@dataclass
class Round:
    """Represents a single round in the Wheel of Fortune game."""
    
    puzzle: Puzzle
    round_number: int
    is_completed: bool = False
    winning_team_id: Optional[str] = None
    round_id: Optional[str] = None
    
    def __post_init__(self):
        """Initialize round after creation."""
        if self.round_id is None:
            self.round_id = str(uuid4())
        
        if self.round_number < 1:
            raise ValueError("Round number must be at least 1")
    
    def complete_round(self, winning_team: 'Team') -> None:
        """
        Mark the round as completed with a winning team.
        
        Args:
            winning_team: The team that won this round
        """
        if self.is_completed:
            raise ValueError("Round is already completed")
        
        self.is_completed = True
        self.winning_team_id = winning_team.team_id
        
        # Award the round money to the winning team
        winning_team.win_round()
    
    def is_puzzle_solved(self) -> bool:
        """Check if the puzzle in this round is solved."""
        return self.puzzle.is_solved()
    
    def get_puzzle_display(self) -> str:
        """Get the current display of the puzzle."""
        return self.puzzle.get_display()
    
    def get_category(self) -> str:
        """Get the puzzle category for this round."""
        return self.puzzle.category
    
    def get_solution(self) -> str:
        """Get the puzzle solution (should only be used when round is completed)."""
        return self.puzzle.solution
    
    def reset_puzzle(self) -> None:
        """Reset the puzzle in this round (clear all guessed letters)."""
        if self.is_completed:
            raise ValueError("Cannot reset puzzle for completed round")
        self.puzzle.reset()
    
    def __str__(self) -> str:
        status = "Completed" if self.is_completed else "In Progress"
        return f"Round {self.round_number} ({status}): {self.puzzle.category}"
    
    def __repr__(self) -> str:
        return f"Round(number={self.round_number}, completed={self.is_completed}, puzzle={self.puzzle.category})" 