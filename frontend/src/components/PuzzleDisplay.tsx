import React from 'react';
import { ImageLetterBoard } from './ImageLetterBoard';
import type { Puzzle } from '../types/game';

interface PuzzleDisplayProps {
  puzzle: Puzzle;
  newlyRevealedLetters?: string[];
}

export const PuzzleDisplay = ({ puzzle, newlyRevealedLetters = [] }: PuzzleDisplayProps) => {
  return (
    <ImageLetterBoard puzzle={puzzle} newlyRevealedLetters={newlyRevealedLetters} />
  );
}; 