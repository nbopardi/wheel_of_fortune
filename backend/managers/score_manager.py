from typing import List, Dict, Optional
from models.team import Team
from models.game import Game


class ScoreManager:
    """Manages scoring and money tracking for Wheel of Fortune game."""
    
    def __init__(self, game: Game):
        """
        Initialize the score manager with a game instance.
        
        Args:
            game: The game instance to manage scores for
        """
        self.game = game
    
    def get_leaderboard(self) -> List[Dict]:
        """
        Get the current leaderboard sorted by total money.
        
        Returns:
            List[Dict]: Leaderboard with team information
        """
        leaderboard = []
        for i, team in enumerate(sorted(self.game.teams, key=lambda t: t.total_money, reverse=True)):
            leaderboard.append({
                "position": i + 1,
                "team_name": team.name,
                "team_id": team.team_id,
                "members": team.members,
                "total_money": team.total_money,
                "current_round_money": team.current_round_money,
                "has_free_spin": team.has_free_spin
            })
        return leaderboard
    
    def get_round_standings(self) -> List[Dict]:
        """
        Get the current round standings sorted by current round money.
        
        Returns:
            List[Dict]: Round standings with team information
        """
        standings = []
        for i, team in enumerate(sorted(self.game.teams, key=lambda t: t.current_round_money, reverse=True)):
            standings.append({
                "position": i + 1,
                "team_name": team.name,
                "team_id": team.team_id,
                "current_round_money": team.current_round_money,
                "total_money": team.total_money
            })
        return standings
    
    def get_team_stats(self, team_id: str) -> Optional[Dict]:
        """
        Get detailed statistics for a specific team.
        
        Args:
            team_id: The ID of the team to get stats for
            
        Returns:
            Dict or None: Team statistics or None if team not found
        """
        team = self._find_team_by_id(team_id)
        if not team:
            return None
        
        # Calculate rounds won
        rounds_won = sum(1 for round_obj in self.game.rounds 
                        if round_obj.is_completed and round_obj.winning_team_id == team_id)
        
        return {
            "team_name": team.name,
            "team_id": team.team_id,
            "members": team.members,
            "total_money": team.total_money,
            "current_round_money": team.current_round_money,
            "rounds_won": rounds_won,
            "has_free_spin": team.has_free_spin,
            "member_count": team.get_member_count()
        }
    
    def get_game_summary(self) -> Dict:
        """
        Get a comprehensive summary of the game's scoring.
        
        Returns:
            Dict: Game summary with all relevant statistics
        """
        total_money_in_play = sum(team.total_money + team.current_round_money for team in self.game.teams)
        highest_total = max(team.total_money for team in self.game.teams) if self.game.teams else 0
        highest_round = max(team.current_round_money for team in self.game.teams) if self.game.teams else 0
        
        completed_rounds = sum(1 for round_obj in self.game.rounds if round_obj.is_completed)
        
        return {
            "game_id": self.game.game_id,
            "total_teams": len(self.game.teams),
            "total_rounds": self.game.total_rounds,
            "completed_rounds": completed_rounds,
            "current_round": self.game.current_round_index + 1,
            "total_money_in_play": total_money_in_play,
            "highest_total_money": highest_total,
            "highest_round_money": highest_round,
            "game_state": self.game.game_state.value,
            "leader": self._get_current_leader(),
            "round_winners": self._get_round_winners()
        }
    
    def calculate_money_earned(self, letter_count: int, wheel_value: int) -> int:
        """
        Calculate money earned from a letter guess.
        
        Args:
            letter_count: Number of times the letter appears in the puzzle
            wheel_value: Value from the wheel spin
            
        Returns:
            int: Total money earned
        """
        return letter_count * wheel_value
    
    def get_money_distribution(self) -> Dict:
        """
        Get the distribution of money across all teams.
        
        Returns:
            Dict: Money distribution statistics
        """
        if not self.game.teams:
            return {"total": 0, "average": 0, "median": 0, "teams": []}
        
        total_money_list = [team.total_money for team in self.game.teams]
        round_money_list = [team.current_round_money for team in self.game.teams]
        
        total_sum = sum(total_money_list)
        round_sum = sum(round_money_list)
        
        return {
            "total_money_awarded": total_sum,
            "current_round_money": round_sum,
            "average_total_per_team": total_sum / len(self.game.teams),
            "average_round_per_team": round_sum / len(self.game.teams),
            "total_money_range": {
                "min": min(total_money_list),
                "max": max(total_money_list)
            },
            "round_money_range": {
                "min": min(round_money_list),
                "max": max(round_money_list)
            }
        }
    
    def reset_round_money(self) -> None:
        """Reset all teams' current round money to 0."""
        for team in self.game.teams:
            team.current_round_money = 0
    
    def award_bonus_money(self, team_id: str, amount: int) -> bool:
        """
        Award bonus money to a specific team.
        
        Args:
            team_id: The ID of the team to award money to
            amount: The amount of money to award
            
        Returns:
            bool: True if successful, False if team not found
        """
        team = self._find_team_by_id(team_id)
        if not team or amount < 0:
            return False
        
        team.add_money(amount)
        return True
    
    def _find_team_by_id(self, team_id: str) -> Optional[Team]:
        """Find a team by its ID."""
        for team in self.game.teams:
            if team.team_id == team_id:
                return team
        return None
    
    def _get_current_leader(self) -> Optional[Dict]:
        """Get the current leading team."""
        if not self.game.teams:
            return None
        
        leader = max(self.game.teams, key=lambda t: t.total_money)
        return {
            "team_name": leader.name,
            "team_id": leader.team_id,
            "total_money": leader.total_money
        }
    
    def _get_round_winners(self) -> List[Dict]:
        """Get the winners of each completed round."""
        winners = []
        for round_obj in self.game.rounds:
            if round_obj.is_completed and round_obj.winning_team_id:
                team = self._find_team_by_id(round_obj.winning_team_id)
                if team:
                    winners.append({
                        "round_number": round_obj.round_number,
                        "team_name": team.name,
                        "team_id": team.team_id,
                        "puzzle_category": round_obj.get_category(),
                        "puzzle_solution": round_obj.get_solution()
                    })
        return winners 