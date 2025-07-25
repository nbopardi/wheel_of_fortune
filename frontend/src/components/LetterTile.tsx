interface LetterTileProps {
  letter?: string;
  isRevealed: boolean;
  isSpace?: boolean;
  isPunctuation?: boolean;
  isNewlyRevealed?: boolean;
}

export const LetterTile = ({ 
  letter, 
  isRevealed, 
  isSpace, 
  isPunctuation, 
  isNewlyRevealed 
}: LetterTileProps) => {
  // Word spacing
  if (isSpace) {
    return <div className="w-4 h-16" />;
  }

  // Punctuation - always visible
  if (isPunctuation || (letter && !letter.match(/[A-Z]/i))) {
    return (
      <div className="w-8 h-16 flex items-center justify-center text-2xl font-bold">
        {letter}
      </div>
    );
  }

  // Letter tile
  const tileClasses = isRevealed 
    ? `letter-tile-revealed ${isNewlyRevealed ? 'ring-2 ring-wof-gold' : ''}` 
    : 'letter-tile-blank';

  return (
    <div className={tileClasses}>
      {isRevealed ? letter?.toUpperCase() : '_'}
    </div>
  );
}; 