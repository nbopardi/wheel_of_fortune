from enum import Enum
from typing import Union


class WheelResult(Enum):
    """Enum representing all possible outcomes from spinning the Wheel of Fortune."""
    
    # Money values (in dollars)
    MONEY_300 = 300
    MONEY_500 = 500
    MONEY_550 = 550
    MONEY_600 = 600
    MONEY_650 = 650
    MONEY_700 = 700
    MONEY_750 = 750
    MONEY_800 = 800
    MONEY_850 = 850
    MONEY_900 = 900
    MONEY_2500 = 2500
    MONEY_5000 = 5000
    
    # Special segments
    BANKRUPT = "BANKRUPT"
    LOSE_A_TURN = "LOSE_A_TURN"
    FREE_SPIN = "FREE_SPIN"
    
    # Prize segments (optional for future expansion)
    PRIZE_TRIP = "PRIZE_TRIP"
    PRIZE_CAR = "PRIZE_CAR"
    
    def is_money(self) -> bool:
        """Check if this wheel result represents a money value."""
        return isinstance(self.value, int)
    
    def is_special(self) -> bool:
        """Check if this wheel result is a special segment."""
        return self.value in ["BANKRUPT", "LOSE_A_TURN", "FREE_SPIN"]
    
    def is_prize(self) -> bool:
        """Check if this wheel result is a prize segment."""
        return self.value in ["PRIZE_TRIP", "PRIZE_CAR"]
    
    def get_money_value(self) -> int:
        """Get the money value if this is a money segment, otherwise return 0."""
        if self.is_money():
            return self.value
        return 0
    
    @classmethod
    def get_all_money_options(cls) -> list['WheelResult']:
        """Get all money value wheel results."""
        return [result for result in cls if result.is_money()]
    
    @classmethod
    def get_all_special_options(cls) -> list['WheelResult']:
        """Get all special segment wheel results."""
        return [result for result in cls if result.is_special()] 