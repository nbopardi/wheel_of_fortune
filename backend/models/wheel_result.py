from enum import Enum
from typing import Union


class WheelResult(Enum):
    """Enum representing all possible outcomes from spinning the Wheel of Fortune."""
    
    # Money values (in dollars)
    MONEY_100 = 100
    MONEY_200 = 200
    MONEY_300 = 300
    MONEY_500 = 500
    MONEY_750 = 750
    MONEY_1000 = 1000
    
    # Special segments
    BANKRUPT = "BANKRUPT"
    LOSE_A_TURN = "LOSE_A_TURN"
    DANCE = "DANCE"  # Team does dance move, gets $1001
    STORY = "STORY"  # Team tells story, gets $1001
    WIN_A_CAR = "WIN_A_CAR"  # Team gets toy car, gets $0
    
    def is_money(self) -> bool:
        """Check if this wheel result represents a money value."""
        return isinstance(self.value, int)
    
    def is_special(self) -> bool:
        """Check if this wheel result is a special segment."""
        return self.value in ["BANKRUPT", "LOSE_A_TURN", "DANCE", "STORY", "WIN_A_CAR"]
    
    def get_money_value(self) -> int:
        """Get the money value if this is a money segment, otherwise return 0."""
        if self.is_money():
            return int(self.value)
        elif self.value == "DANCE" or self.value == "STORY":
            return 1001
        else:
            return 0
    
    @classmethod
    def get_all_money_options(cls) -> list['WheelResult']:
        """Get all money value wheel results."""
        return [result for result in cls if result.is_money()]
    
    @classmethod
    def get_all_special_options(cls) -> list['WheelResult']:
        """Get all special segment wheel results."""
        return [result for result in cls if result.is_special()] 