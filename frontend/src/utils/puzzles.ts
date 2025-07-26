import type { Puzzle } from '../types/game';
import puzzlesData from '../data/puzzles.json';

export interface PuzzleData {
  solution: string;
  category: string;
}

// Function to generate the display string with underscores
function generatePuzzleDisplay(solution: string): string {
  return solution
    .split('')
    .map(char => {
      if (char.match(/[A-Z]/i)) {
        return '_';
      } else if (char === ' ') {
        return '  '; // Double space for word breaks
      } else {
        return char; // Keep punctuation as-is
      }
    })
    .join(' '); // Add space between each character/underscore
}

// Function to convert basic puzzle data to full Puzzle interface
export function createPuzzle(puzzleData: PuzzleData): Puzzle {
  return {
    solution: puzzleData.solution,
    category: puzzleData.category,
    guessed_letters: [],
    display: generatePuzzleDisplay(puzzleData.solution),
    available_consonants: ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"],
    available_vowels: ["A", "E", "I", "O", "U"]
  };
}

// Function to get all puzzles
export function getAllPuzzles(): PuzzleData[] {
  return puzzlesData;
}

// Function to get a random puzzle
export function getRandomPuzzle(): PuzzleData {
  const puzzles = getAllPuzzles();
  const randomIndex = Math.floor(Math.random() * puzzles.length);
  return puzzles[randomIndex];
}

// Function to get a puzzle by index (cycling if necessary)
export function getPuzzleByIndex(index: number): PuzzleData {
  const puzzles = getAllPuzzles();
  const puzzleIndex = index % puzzles.length;
  return puzzles[puzzleIndex];
}

// Function to get the first puzzle (for game initialization)
export function getInitialPuzzle(): PuzzleData {
  const puzzles = getAllPuzzles();
  return puzzles[0]; // Return the first puzzle
} 