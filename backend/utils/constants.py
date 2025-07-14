# Game constants for Wheel of Fortune

# Cost to buy a vowel (in dollars)
VOWEL_COST = 250

# Default number of rounds per game
DEFAULT_TOTAL_ROUNDS = 3

# Maximum number of teams allowed
MAX_TEAMS = 6

# Minimum number of teams required
MIN_TEAMS = 2

# All vowels
VOWELS = set("AEIOU")

# All consonants
CONSONANTS = set("BCDFGHJKLMNPQRSTVWXYZ")

# All letters
ALL_LETTERS = VOWELS | CONSONANTS

# Puzzle categories
PUZZLE_CATEGORIES = [
    "BEFORE & AFTER",
    "PHRASE",
    "MOVIE TITLE",
    "TV SHOW",
    "PERSON",
    "PLACE",
    "THING",
    "EVENT",
    "QUOTATION",
    "SONG LYRICS",
    "FOOD & DRINK",
    "LIVING THING",
    "OCCUPATION",
    "PROPER NAME",
    "WHAT ARE YOU DOING?",
    "AROUND THE HOUSE",
    "FUN & GAMES",
    "ON THE MAP",
    "RHYME TIME",
    "SAME LETTER",
    "SAME NAME"
] 