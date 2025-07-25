import React from 'react';
import type { Puzzle } from '../types/game';

const ROW_CAPACITIES = [12, 12, 12, 12]; // All rows have 12 slots

// Manual coordinate mapping for precise letter positioning
// Format: 'row-col': { x: 'X%', y: 'Y%' }
// TODO: Replace with actual coordinates from Firefox dev tools
const LETTER_SLOT_COORDINATES: { [key: string]: { x: string; y: string } } = {
  // Row 1 (12 slots)
  '0-0': { x: '18.1%', y: '31.8%' },  // Slot 1
  '0-1': { x: '23.9%', y: '31.8%' },  // Slot 2
  '0-2': { x: '29.8%', y: '31.8%' },  // Slot 3
  '0-3': { x: '35.7%', y: '31.9%' },  // Slot 4
  '0-4': { x: '41.6%', y: '31.8%' },  // Slot 5
  '0-5': { x: '47.65%', y: '31.8%' },  // Slot 6
  '0-6': { x: '53.5%', y: '31.8%' },  // Slot 7
  '0-7': { x: '59.4%', y: '31.8%' },  // Slot 8
  '0-8': { x: '65.2%', y: '31.8%' },  // Slot 9 
  '0-9': { x: '71.1%', y: '31.8%' },  // Slot 10
  '0-10': { x: '76.7%', y: '31.8%' }, // Slot 11 
  '0-11': { x: '82.2%', y: '31.8%' }, // Slot 12 
  
  // Row 2 (12 slots)
  '1-0': { x: '18.2%', y: '47.5%' },  // Slot 1
  '1-1': { x: '24.0%', y: '47.5%' },  // Slot 2
  '1-2': { x: '29.8%', y: '47.5%' },  // Slot 3
  '1-3': { x: '35.7%', y: '47.5%' },  // Slot 4
  '1-4': { x: '41.7%', y: '47.5%' },  // Slot 5
  '1-5': { x: '47.65%', y: '47.5%' },  // Slot 6
  '1-6': { x: '53.5%', y: '47.5%' },  // Slot 7
  '1-7': { x: '59.4%', y: '47.5%' },  // Slot 8
  '1-8': { x: '65.2%', y: '47.5%' },  // Slot 9
  '1-9': { x: '71.1%', y: '47.5%' },  // Slot 10
  '1-10': { x: '76.7%', y: '47.5%' }, // Slot 11
  '1-11': { x: '82.2%', y: '47.5%' }, // Slot 12

  // Row 3 (12 slots)
  '2-0': { x: '18.2%', y: '63.2%' },  // Slot 1 
  '2-1': { x: '24.1%', y: '63.2%' },  // Slot 2
  '2-2': { x: '29.9%', y: '63.2%' },  // Slot 3 
  '2-3': { x: '35.7%', y: '63.2%' },  // Slot 4 
  '2-4': { x: '41.7%', y: '63.2%' },  // Slot 5 
  '2-5': { x: '47.65%', y: '63.2%' },  // Slot 6
  '2-6': { x: '53.5%', y: '63.2%' },  // Slot 7 
  '2-7': { x: '59.4%', y: '63.2%' },  // Slot 8 
  '2-8': { x: '65.2%', y: '63.2%' },  // Slot 9 
  '2-9': { x: '71.1%', y: '63.2%' },  // Slot 10 
  '2-10': { x: '76.7%', y: '63.2%' }, // Slot 11
  '2-11': { x: '82.2%', y: '63.2%' }, // Slot 12

  // Row 4 (12 slots)
  '3-0': { x: '18.4%', y: '79.0%' },  // Slot 1 
  '3-1': { x: '24.1%', y: '79.0%' },  // Slot 2 
  '3-2': { x: '30.0%', y: '79.0%' },  // Slot 3 
  '3-3': { x: '35.9%', y: '79.0%' },  // Slot 4 
  '3-4': { x: '41.8%', y: '79.0%' },  // Slot 5
  '3-5': { x: '47.65%', y: '79.0%' },  // Slot 6
  '3-6': { x: '53.5%', y: '79.0%' },  // Slot 7 
  '3-7': { x: '59.4%', y: '79.0%' },  // Slot 8 
  '3-8': { x: '65.2%', y: '79.0%' },  // Slot 9 
  '3-9': { x: '71.1%', y: '79.0%' },  // Slot 10 
  '3-10': { x: '76.7%', y: '79.0%' }, // Slot 11 
  '3-11': { x: '82.2%', y: '78.9%' }, // Slot 12
};

interface LetterPosition {
  char: string;
  rowIndex: number;
  colIndex: number;
}

interface ImageLetterBoardProps {
  puzzle: Puzzle;
  newlyRevealedLetters?: string[];
}

export const ImageLetterBoard = ({ puzzle, newlyRevealedLetters = [] }: ImageLetterBoardProps) => {
  const assignWordsToRows = (solution: string): LetterPosition[] => {
    const positions: LetterPosition[] = [];
    const words = solution.split(' ');
    
    let currentRow = 0;
    let currentPosition = 0; // Position within current row
    
    words.forEach((word, wordIndex) => {
      const wordLength = word.length;
      const needsSpace = currentPosition > 0; // Need space before word if not first on row
      const totalNeeded = wordLength + (needsSpace ? 1 : 0);
      
      // Check if word fits on current row
      if (currentPosition + totalNeeded > ROW_CAPACITIES[currentRow] && currentPosition > 0) {
        // Move to next row
        currentRow++;
        currentPosition = 0;
        
        // Safety check - don't exceed available rows
        if (currentRow >= ROW_CAPACITIES.length) {
          console.warn('Puzzle too long for board layout');
          return;
        }
      }
      
      // Add space if needed (not first word on row)
      if (currentPosition > 0 && wordIndex > 0) {
        // Space is invisible, just increment position
        currentPosition++;
      }
      
      // Add letters of the word
      for (let i = 0; i < word.length; i++) {
        if (currentPosition < ROW_CAPACITIES[currentRow]) {
          positions.push({
            char: word[i],
            rowIndex: currentRow,
            colIndex: currentPosition,
          });
          currentPosition++;
        }
      }
    });
    
    return positions;
  };

  const getLetterImagePath = (char: string, isRevealed: boolean, isPunctuation: boolean): string | null => {
    if (isPunctuation) {
      // Map punctuation to specific images
      const punctuationMap: { [key: string]: string } = {
        "'": 'apostrophe',
        '-': 'hyphen',
        '&': 'ampersand',
        ':': 'colon',
        '?': 'question',
      };
      
      const punctuationFile = punctuationMap[char];
      if (punctuationFile) {
        return `/assets/letter_board/letters/letter_${punctuationFile}.png`;
      }
    }
    
    if (!isRevealed) {
      return '/assets/letter_board/letters/letter_blank.png';
    }
    
    // Map revealed letters to image files
    const letterFile = char.toLowerCase();
    return `/assets/letter_board/letters/letter_${letterFile}.png`;
  };

  const letterPositions = assignWordsToRows(puzzle.solution);

  return (
    <div className="flex flex-col items-center space-y-6 p-4">
      {/* Category Banner */}
      <div className="bg-wof-blue text-white px-8 py-3 rounded-lg text-xl font-bold shadow-lg">
        {puzzle.category}
      </div>
      
      {/* Letter Board Container */}
      <div className="relative w-full max-w-6xl mx-auto">
        {/* Background board image */}
        <img 
          src="/assets/letter_board/letter_board.png" 
          alt="Wheel of Fortune Letter Board"
          className="w-full h-auto block"
          style={{ 
            maxWidth: '1400px',
            width: '100%',
            height: 'auto'
          }}
        />
        
        {/* Absolute Positioned Letter Tiles */}
        <div 
          className="absolute" 
          style={{ 
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            zIndex: 10
          }}
        >
          {/* Only show tiles where there are actual letters */}
          {letterPositions.map((position, index) => {
            const coordinateKey = `${position.rowIndex}-${position.colIndex}`;
            const coordinates = LETTER_SLOT_COORDINATES[coordinateKey];
            
            // Skip if no coordinates mapped for this position
            if (!coordinates) {
              console.warn(`No coordinates found for slot ${coordinateKey}`);
              return null;
            }
            
            const isPunctuation = !position.char.match(/[A-Z]/i);
            const isRevealed = puzzle.guessed_letters.includes(position.char.toUpperCase()) || isPunctuation;
            const isNewlyRevealed = newlyRevealedLetters.includes(position.char.toUpperCase());
            const imagePath = getLetterImagePath(position.char, isRevealed, isPunctuation);
            
            if (!imagePath) {
              console.warn(`No image path for character: ${position.char}`);
              return null;
            }
            
            return (
              <img
                key={index}
                src={imagePath}
                alt={isRevealed ? position.char.toUpperCase() : 'Hidden letter'}
                className={`absolute transition-all duration-300 ${
                  isNewlyRevealed ? 'animate-pulse ring-2 ring-yellow-400' : ''
                }`}
                style={{
                  left: coordinates.x,
                  top: coordinates.y,
                  width: '55px',
                  height: '70px',
                  transform: 'translate(-50%, -50%)',
                  filter: 'drop-shadow(1px 1px 2px rgba(0, 0, 0, 0.3))',
                  zIndex: 15
                }}
                onError={(e) => {
                  console.warn(`Failed to load image: ${imagePath}`);
                  e.currentTarget.style.display = 'none';
                }}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}; 