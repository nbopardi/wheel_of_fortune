from typing import Set, List
from dataclasses import dataclass, field
import re


@dataclass
class Puzzle:
    """Represents a word puzzle in the Wheel of Fortune game."""
    
    solution: str
    category: str
    guessed_letters: Set[str] = field(default_factory=set)
    
    def __post_init__(self):
        """Validate puzzle data after initialization."""
        if not self.solution.strip():
            raise ValueError("Puzzle solution cannot be empty")
        if not self.category.strip():
            raise ValueError("Puzzle category cannot be empty")
        
        # Normalize solution to uppercase for consistency
        self.solution = self.solution.upper().strip()
        self.category = self.category.upper().strip()
    
    def get_display(self) -> str:
        """Get the current display of the puzzle with guessed letters revealed."""
        display = ""
        for char in self.solution:
            if char.isalpha():
                if char in self.guessed_letters:
                    display += char
                else:
                    display += "_"
            else:
                # Show punctuation, spaces, and numbers
                display += char
        return display
    
    def guess_letter(self, letter: str) -> bool:
        """
        Guess a letter and return True if it's in the puzzle.
        
        Args:
            letter: The letter to guess (will be normalized to uppercase)
            
        Returns:
            bool: True if the letter is in the puzzle, False otherwise
            
        Raises:
            ValueError: If the letter is invalid or already guessed
        """
        letter = letter.upper().strip()
        
        # Validate input
        if len(letter) != 1 or not letter.isalpha():
            raise ValueError("Must guess exactly one letter")
        
        if letter in self.guessed_letters:
            raise ValueError(f"Letter '{letter}' has already been guessed")
        
        # Add to guessed letters
        self.guessed_letters.add(letter)
        
        # Check if letter is in the solution
        return letter in self.solution
    
    def count_letter_occurrences(self, letter: str) -> int:
        """Count how many times a letter appears in the solution."""
        letter = letter.upper().strip()
        return self.solution.count(letter)
    
    def is_vowel(self, letter: str) -> bool:
        """Check if a letter is a vowel."""
        return letter.upper() in "AEIOU"
    
    def is_consonant(self, letter: str) -> bool:
        """Check if a letter is a consonant."""
        return letter.isalpha() and not self.is_vowel(letter)
    
    def get_available_consonants(self) -> Set[str]:
        """Get all consonants that haven't been guessed yet."""
        all_consonants = set("BCDFGHJKLMNPQRSTVWXYZ")
        return all_consonants - self.guessed_letters
    
    def get_available_vowels(self) -> Set[str]:
        """Get all vowels that haven't been guessed yet."""
        all_vowels = set("AEIOU")
        return all_vowels - self.guessed_letters
    
    def is_solved(self) -> bool:
        """Check if the puzzle is completely solved."""
        for char in self.solution:
            if char.isalpha() and char not in self.guessed_letters:
                return False
        return True
    
    def attempt_solve(self, guess: str) -> bool:
        """
        Attempt to solve the puzzle with a complete guess.
        
        Args:
            guess: The complete solution guess
            
        Returns:
            bool: True if the guess matches the solution
        """
        guess = guess.upper().strip()
        return guess == self.solution
    
    def get_remaining_letters(self) -> int:
        """Get the number of unique letters still to be guessed."""
        unique_letters = set(char for char in self.solution if char.isalpha())
        return len(unique_letters - self.guessed_letters)
    
    def get_revealed_percentage(self) -> float:
        """Get the percentage of letters that have been revealed."""
        unique_letters = set(char for char in self.solution if char.isalpha())
        if not unique_letters:
            return 100.0
        
        revealed_letters = unique_letters & self.guessed_letters
        return (len(revealed_letters) / len(unique_letters)) * 100
    
    def reset(self) -> None:
        """Reset the puzzle by clearing all guessed letters."""
        self.guessed_letters.clear()
    
    def __str__(self) -> str:
        return f"Category: {self.category}\nPuzzle: {self.get_display()}"
    
    def __repr__(self) -> str:
        return f"Puzzle(solution='{self.solution}', category='{self.category}', guessed={self.guessed_letters})" 