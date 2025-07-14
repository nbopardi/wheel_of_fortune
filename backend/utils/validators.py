import re
from typing import List
from .constants import ALL_LETTERS, VOWELS, CONSONANTS


def validate_team_name(name: str) -> bool:
    """
    Validate a team name.
    
    Args:
        name: The team name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not name or not name.strip():
        return False
    
    # Check length (reasonable limits)
    if len(name.strip()) < 1 or len(name.strip()) > 50:
        return False
    
    # Check for valid characters (letters, numbers, spaces, basic punctuation)
    if not re.match(r'^[a-zA-Z0-9\s\-_\'\.]+$', name.strip()):
        return False
    
    return True


def validate_letter(letter: str) -> bool:
    """
    Validate a single letter input.
    
    Args:
        letter: The letter to validate
        
    Returns:
        bool: True if valid letter, False otherwise
    """
    if not letter or len(letter.strip()) != 1:
        return False
    
    return letter.upper().strip() in ALL_LETTERS


def validate_member_name(name: str) -> bool:
    """
    Validate a team member name.
    
    Args:
        name: The member name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not name or not name.strip():
        return False
    
    # Check length
    if len(name.strip()) < 1 or len(name.strip()) > 30:
        return False
    
    # Check for valid characters
    if not re.match(r'^[a-zA-Z\s\-\'\.]+$', name.strip()):
        return False
    
    return True


def validate_puzzle_solution(solution: str) -> bool:
    """
    Validate a puzzle solution.
    
    Args:
        solution: The puzzle solution to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not solution or not solution.strip():
        return False
    
    # Check length
    if len(solution.strip()) < 3 or len(solution.strip()) > 100:
        return False
    
    # Must contain at least one letter
    if not any(c.isalpha() for c in solution):
        return False
    
    return True


def validate_category(category: str) -> bool:
    """
    Validate a puzzle category.
    
    Args:
        category: The category to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not category or not category.strip():
        return False
    
    # Check length
    if len(category.strip()) < 3 or len(category.strip()) > 50:
        return False
    
    return True


def is_vowel(letter: str) -> bool:
    """Check if a letter is a vowel."""
    return letter.upper().strip() in VOWELS


def is_consonant(letter: str) -> bool:
    """Check if a letter is a consonant."""
    return letter.upper().strip() in CONSONANTS


def sanitize_input(text: str) -> str:
    """
    Sanitize text input by trimming and normalizing.
    
    Args:
        text: The text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    return text.strip().upper() 