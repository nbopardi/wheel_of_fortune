import json
import random
from typing import List, Dict, Optional
from pathlib import Path

from models.puzzle import Puzzle
from utils.validators import validate_puzzle_solution, validate_category


class PuzzleManager:
    """Manages puzzles for the Wheel of Fortune game."""
    
    def __init__(self, data_dir: str = "backend/data"):
        """
        Initialize the puzzle manager.
        
        Args:
            data_dir: Directory containing puzzle data files
        """
        self.data_dir = Path(data_dir)
        self.puzzles: List[Dict] = []
        self.categories: List[str] = []
        self._load_data()
    
    def _load_data(self) -> None:
        """Load puzzle data from JSON files."""
        try:
            # Load puzzles
            puzzles_file = self.data_dir / "puzzles.json"
            if puzzles_file.exists():
                with open(puzzles_file, 'r') as f:
                    self.puzzles = json.load(f)
            else:
                # Create default puzzles if file doesn't exist
                self._create_default_puzzles()
            
            # Load categories
            categories_file = self.data_dir / "categories.json"
            if categories_file.exists():
                with open(categories_file, 'r') as f:
                    self.categories = json.load(f)
            else:
                # Extract categories from puzzles
                self.categories = list(set(puzzle["category"] for puzzle in self.puzzles))
                
        except Exception as e:
            print(f"Error loading puzzle data: {e}")
            self._create_default_puzzles()
    
    def _create_default_puzzles(self) -> None:
        """Create a default set of puzzles for testing."""
        self.puzzles = [
            {"solution": "WHEEL OF FORTUNE", "category": "TV SHOW"},
            {"solution": "THE QUICK BROWN FOX", "category": "PHRASE"},
            {"solution": "PIZZA AND SODA", "category": "FOOD & DRINK"},
            {"solution": "HAPPY BIRTHDAY", "category": "PHRASE"},
            {"solution": "NEW YORK CITY", "category": "PLACE"},
            {"solution": "STAR WARS", "category": "MOVIE TITLE"},
            {"solution": "BASKETBALL PLAYER", "category": "OCCUPATION"},
            {"solution": "CHOCOLATE CHIP COOKIES", "category": "FOOD & DRINK"},
            {"solution": "GOOD MORNING AMERICA", "category": "TV SHOW"},
            {"solution": "ROCK AND ROLL", "category": "PHRASE"},
            {"solution": "THANKSGIVING DINNER", "category": "EVENT"},
            {"solution": "SUPER BOWL SUNDAY", "category": "EVENT"},
            {"solution": "COFFEE AND DONUTS", "category": "FOOD & DRINK"},
            {"solution": "PIECE OF CAKE", "category": "PHRASE"},
            {"solution": "BREAKING NEWS", "category": "PHRASE"},
            {"solution": "HOLLYWOOD MOVIES", "category": "THING"},
            {"solution": "SUMMER VACATION", "category": "EVENT"},
            {"solution": "WINTER WONDERLAND", "category": "PHRASE"},
            {"solution": "FRESH AS A DAISY", "category": "PHRASE"},
            {"solution": "KITCHEN SINK", "category": "AROUND THE HOUSE"}
        ]
        
        # Save default puzzles
        self._save_puzzles()
    
    def _save_puzzles(self) -> None:
        """Save puzzles to JSON file."""
        try:
            self.data_dir.mkdir(exist_ok=True)
            puzzles_file = self.data_dir / "puzzles.json"
            with open(puzzles_file, 'w') as f:
                json.dump(self.puzzles, f, indent=2)
        except Exception as e:
            print(f"Error saving puzzles: {e}")
    
    def get_random_puzzle(self, category: Optional[str] = None) -> Puzzle:
        """
        Get a random puzzle, optionally filtered by category.
        
        Args:
            category: Optional category to filter by
            
        Returns:
            Puzzle: A random puzzle object
        """
        available_puzzles = self.puzzles
        
        if category:
            available_puzzles = [p for p in self.puzzles if p["category"].upper() == category.upper()]
            
        if not available_puzzles:
            raise ValueError(f"No puzzles available for category: {category}")
        
        puzzle_data = random.choice(available_puzzles)
        return Puzzle(solution=puzzle_data["solution"], category=puzzle_data["category"])
    
    def get_puzzle_by_solution(self, solution: str) -> Optional[Puzzle]:
        """
        Get a specific puzzle by its solution.
        
        Args:
            solution: The puzzle solution to search for
            
        Returns:
            Puzzle or None: The puzzle if found, None otherwise
        """
        for puzzle_data in self.puzzles:
            if puzzle_data["solution"].upper() == solution.upper():
                return Puzzle(solution=puzzle_data["solution"], category=puzzle_data["category"])
        return None
    
    def get_puzzles_by_category(self, category: str) -> List[Puzzle]:
        """
        Get all puzzles for a specific category.
        
        Args:
            category: The category to search for
            
        Returns:
            List[Puzzle]: List of puzzles in the category
        """
        puzzles = []
        for puzzle_data in self.puzzles:
            if puzzle_data["category"].upper() == category.upper():
                puzzles.append(Puzzle(solution=puzzle_data["solution"], category=puzzle_data["category"]))
        return puzzles
    
    def add_puzzle(self, solution: str, category: str) -> bool:
        """
        Add a new puzzle to the collection.
        
        Args:
            solution: The puzzle solution
            category: The puzzle category
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        if not validate_puzzle_solution(solution) or not validate_category(category):
            return False
        
        # Check if puzzle already exists
        if any(p["solution"].upper() == solution.upper() for p in self.puzzles):
            return False
        
        self.puzzles.append({
            "solution": solution.upper().strip(),
            "category": category.upper().strip()
        })
        
        # Update categories list
        if category.upper().strip() not in [c.upper() for c in self.categories]:
            self.categories.append(category.upper().strip())
        
        self._save_puzzles()
        return True
    
    def get_all_categories(self) -> List[str]:
        """Get all available puzzle categories."""
        return sorted(self.categories)
    
    def get_puzzle_count(self) -> int:
        """Get the total number of puzzles."""
        return len(self.puzzles)
    
    def get_puzzle_count_by_category(self, category: str) -> int:
        """Get the number of puzzles in a specific category."""
        return len([p for p in self.puzzles if p["category"].upper() == category.upper()])
    
    def remove_puzzle(self, solution: str) -> bool:
        """
        Remove a puzzle by its solution.
        
        Args:
            solution: The solution of the puzzle to remove
            
        Returns:
            bool: True if removed successfully, False if not found
        """
        for i, puzzle_data in enumerate(self.puzzles):
            if puzzle_data["solution"].upper() == solution.upper():
                del self.puzzles[i]
                self._save_puzzles()
                return True
        return False 