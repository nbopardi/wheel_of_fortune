from typing import List
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Team:
    """Represents a team in the Wheel of Fortune game."""
    
    name: str
    members: List[str] = field(default_factory=list)
    current_round_money: int = 0
    total_money: int = 0
    has_free_spin: bool = False
    team_id: str = field(default_factory=lambda: str(uuid4()))
    
    def __post_init__(self):
        """Validate team data after initialization."""
        if not self.name.strip():
            raise ValueError("Team name cannot be empty")
        if len(self.members) == 0:
            raise ValueError("Team must have at least one member")
    
    def add_member(self, member_name: str) -> None:
        """Add a member to the team."""
        if not member_name.strip():
            raise ValueError("Member name cannot be empty")
        if member_name in self.members:
            raise ValueError(f"Member '{member_name}' is already on the team")
        self.members.append(member_name)
    
    def remove_member(self, member_name: str) -> None:
        """Remove a member from the team."""
        if member_name not in self.members:
            raise ValueError(f"Member '{member_name}' is not on the team")
        if len(self.members) <= 1:
            raise ValueError("Cannot remove member - team must have at least one member")
        self.members.remove(member_name)
    
    def add_money(self, amount: int) -> None:
        """Add money to the team's current round total."""
        if amount < 0:
            raise ValueError("Cannot add negative money")
        self.current_round_money += amount
    
    def lose_round_money(self) -> None:
        """Lose all money for the current round (e.g., from BANKRUPT)."""
        self.current_round_money = 0
    
    def win_round(self) -> None:
        """Win the round - add current round money to total and reset round money."""
        self.total_money += self.current_round_money
        self.current_round_money = 0
    
    def can_buy_vowel(self, vowel_cost: int = 250) -> bool:
        """Check if the team has enough money to buy a vowel."""
        return self.current_round_money >= vowel_cost
    
    def buy_vowel(self, vowel_cost: int = 250) -> None:
        """Buy a vowel by deducting the cost from current round money."""
        if not self.can_buy_vowel(vowel_cost):
            raise ValueError(f"Not enough money to buy vowel. Need ${vowel_cost}, have ${self.current_round_money}")
        self.current_round_money -= vowel_cost
    
    def use_free_spin(self) -> None:
        """Use the free spin if available."""
        if not self.has_free_spin:
            raise ValueError("Team does not have a free spin")
        self.has_free_spin = False
    
    def give_free_spin(self) -> None:
        """Give the team a free spin."""
        self.has_free_spin = True
    
    def get_member_count(self) -> int:
        """Get the number of members on the team."""
        return len(self.members)
    
    def __str__(self) -> str:
        return f"Team {self.name}: ${self.current_round_money} (Total: ${self.total_money})"
    
    def __repr__(self) -> str:
        return f"Team(name='{self.name}', members={self.members}, current_money={self.current_round_money}, total_money={self.total_money})" 