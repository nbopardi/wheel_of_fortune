import React, { useState } from 'react';
import type { GameStatus } from '../types/game';

interface GameControlsProps {
  gameStatus: GameStatus;
  onSpin?: () => void;
  onGuessLetter?: (letter: string) => void;
  onSolve?: (solution: string) => void;
}

export const GameControls = ({ gameStatus, onSpin, onGuessLetter, onSolve }: GameControlsProps) => {
  const [selectedLetter, setSelectedLetter] = useState('');
  const [solutionGuess, setSolutionGuess] = useState('');
  const [showSolveInput, setShowSolveInput] = useState(false);

  const { current_puzzle, turn_state, teams } = gameStatus;
  const currentTeam = teams.find(team => team.is_current_turn);

  if (!current_puzzle || !currentTeam) {
    return null;
  }

  const canSpin = turn_state === 'WAITING_FOR_SPIN';
  const canGuessLetter = turn_state === 'WAITING_FOR_LETTER_GUESS';
  const canSolve = turn_state === 'WAITING_FOR_SOLVE_ATTEMPT' || turn_state === 'WAITING_FOR_LETTER_GUESS';

  const handleSpin = () => {
    if (onSpin && canSpin) {
      onSpin();
    }
  };

  const handleLetterGuess = () => {
    if (onGuessLetter && selectedLetter && canGuessLetter) {
      onGuessLetter(selectedLetter);
      setSelectedLetter('');
    }
  };

  const handleSolveAttempt = () => {
    if (onSolve && solutionGuess.trim()) {
      onSolve(solutionGuess.trim());
      setSolutionGuess('');
      setShowSolveInput(false);
    }
  };

  const availableConsonants = current_puzzle.available_consonants || [];
  const availableVowels = current_puzzle.available_vowels || [];

  return (
    <div className="bg-white rounded-lg p-6 shadow-lg">
      <div className="text-center mb-6">
        <h3 className="text-xl font-bold text-wof-blue mb-2">
          {currentTeam.name}'s Turn
        </h3>
        <p className="text-gray-600 capitalize">
          {turn_state.replace('_', ' ').toLowerCase()}
        </p>
        {gameStatus.last_wheel_result && (
          <div className="mt-2 px-4 py-2 bg-wof-gold bg-opacity-20 rounded-lg">
            <span className="font-bold text-wof-blue">
              Last Spin: ${gameStatus.last_wheel_result}
            </span>
          </div>
        )}
      </div>

      {/* Spin Wheel Button */}
      {canSpin && (
        <div className="text-center mb-6">
          <button
            onClick={handleSpin}
            className="btn-primary text-lg px-8 py-3 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
          >
            🎡 Spin the Wheel
          </button>
        </div>
      )}

      {/* Letter Guessing */}
      {canGuessLetter && (
        <div className="mb-6">
          <h4 className="font-semibold text-gray-800 mb-3">Choose a Letter:</h4>
          
          {/* Consonants */}
          <div className="mb-4">
            <p className="text-sm text-gray-600 mb-2">Consonants:</p>
            <div className="flex flex-wrap gap-2">
              {availableConsonants.map((letter) => (
                <button
                  key={letter}
                  onClick={() => setSelectedLetter(letter)}
                  className={`w-10 h-10 border-2 rounded font-bold transition-all ${
                    selectedLetter === letter
                      ? 'bg-wof-blue text-white border-wof-blue'
                      : 'bg-white text-gray-800 border-gray-300 hover:border-wof-blue'
                  }`}
                >
                  {letter}
                </button>
              ))}
            </div>
          </div>

          {/* Vowels */}
          <div className="mb-4">
            <p className="text-sm text-gray-600 mb-2">Vowels ($250 each):</p>
            <div className="flex flex-wrap gap-2">
              {availableVowels.map((letter) => (
                <button
                  key={letter}
                  onClick={() => setSelectedLetter(letter)}
                  className={`w-10 h-10 border-2 rounded font-bold transition-all ${
                    selectedLetter === letter
                      ? 'bg-wof-gold text-white border-wof-gold'
                      : 'bg-white text-gray-800 border-gray-300 hover:border-wof-gold'
                  }`}
                >
                  {letter}
                </button>
              ))}
            </div>
          </div>

          {/* Guess Letter Button */}
          {selectedLetter && (
            <div className="text-center">
              <button
                onClick={handleLetterGuess}
                className="btn-secondary px-6 py-2 rounded-lg"
              >
                Guess "{selectedLetter}"
              </button>
            </div>
          )}
        </div>
      )}

      {/* Solve Puzzle */}
      {canSolve && (
        <div className="border-t pt-4">
          {!showSolveInput ? (
            <div className="text-center">
              <button
                onClick={() => setShowSolveInput(true)}
                className="btn-primary px-6 py-2 rounded-lg"
              >
                🎯 Solve the Puzzle
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              <input
                type="text"
                value={solutionGuess}
                onChange={(e) => setSolutionGuess(e.target.value)}
                placeholder="Enter your solution..."
                className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-wof-blue focus:outline-none"
                autoFocus
              />
              <div className="flex gap-2 justify-center">
                <button
                  onClick={handleSolveAttempt}
                  disabled={!solutionGuess.trim()}
                  className="btn-primary px-4 py-2 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Submit
                </button>
                <button
                  onClick={() => {
                    setShowSolveInput(false);
                    setSolutionGuess('');
                  }}
                  className="btn-secondary px-4 py-2 rounded"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Game State Help */}
      <div className="mt-4 text-xs text-gray-500 text-center">
        {turn_state === 'WAITING_FOR_SPIN' && 'Click "Spin the Wheel" to begin your turn'}
        {turn_state === 'WAITING_FOR_LETTER_GUESS' && 'Choose a letter to guess'}
        {turn_state === 'WAITING_FOR_SOLVE_ATTEMPT' && 'Try to solve the puzzle or guess another letter'}
        {turn_state === 'TURN_ENDED' && 'Turn completed, waiting for next player'}
      </div>
    </div>
  );
}; 