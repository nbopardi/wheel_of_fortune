import React, { useState } from 'react';
import { TeamDisplay } from './TeamDisplay';
import { PuzzleDisplay } from './PuzzleDisplay';
import { GameControls } from './GameControls';
import type { GameStatus } from '../types/game';

interface GameBoardProps {
  gameStatus: GameStatus | null;
  isLoading?: boolean;
  error?: string | null;
}

export const GameBoard = ({ gameStatus: initialGameStatus, isLoading, error }: GameBoardProps) => {
  // Local state for demo functionality
  const [gameStatus, setGameStatus] = useState(initialGameStatus);
  const [newlyRevealedLetters, setNewlyRevealedLetters] = useState<string[]>([]);

  // Mock wheel values for demonstration
  const wheelValues = [500, 600, 700, 800, 900, 1000, 1500, 2000, 'BANKRUPT', 'LOSE A TURN'];

  const handleSpin = () => {
    if (!gameStatus) return;

    // Simulate wheel spin with random result
    const randomIndex = Math.floor(Math.random() * wheelValues.length);
    const spinResult = wheelValues[randomIndex];

    setGameStatus(prev => prev ? {
      ...prev,
      last_wheel_result: spinResult,
      turn_state: typeof spinResult === 'number' ? 'WAITING_FOR_LETTER_GUESS' : 'TURN_ENDED'
    } : null);
  };

  const handleGuessLetter = (letter: string) => {
    if (!gameStatus || !gameStatus.current_puzzle) return;

    const puzzle = gameStatus.current_puzzle;
    const isCorrect = puzzle.solution.toUpperCase().includes(letter.toUpperCase());

    if (isCorrect) {
      // Add letter to guessed letters and show as newly revealed
      setNewlyRevealedLetters([letter.toUpperCase()]);
      
      setTimeout(() => {
        setNewlyRevealedLetters([]);
      }, 2000);

      setGameStatus(prev => prev ? {
        ...prev,
        current_puzzle: {
          ...prev.current_puzzle,
          guessed_letters: [...prev.current_puzzle.guessed_letters, letter.toUpperCase()],
          available_consonants: prev.current_puzzle.available_consonants.filter(l => l !== letter.toUpperCase()),
          available_vowels: prev.current_puzzle.available_vowels.filter(l => l !== letter.toUpperCase())
        },
        turn_state: 'WAITING_FOR_SPIN' // Player continues
      } : null);
    } else {
      // Letter not in puzzle - end turn
      setGameStatus(prev => prev ? {
        ...prev,
        current_puzzle: {
          ...prev.current_puzzle,
          available_consonants: prev.current_puzzle.available_consonants.filter(l => l !== letter.toUpperCase()),
          available_vowels: prev.current_puzzle.available_vowels.filter(l => l !== letter.toUpperCase())
        },
        turn_state: 'TURN_ENDED'
      } : null);
    }
  };

  const handleSolve = (solution: string) => {
    if (!gameStatus || !gameStatus.current_puzzle) return;

    const isCorrect = solution.toUpperCase() === gameStatus.current_puzzle.solution.toUpperCase();

    if (isCorrect) {
      // Reveal all letters
      const allLetters = gameStatus.current_puzzle.solution.split('').filter(char => char.match(/[A-Z]/i));
      setGameStatus(prev => prev ? {
        ...prev,
        current_puzzle: {
          ...prev.current_puzzle,
          guessed_letters: allLetters.map(l => l.toUpperCase())
        },
        game_state: 'ROUND_COMPLETED'
      } : null);
    } else {
      // Wrong solution - end turn
      setGameStatus(prev => prev ? {
        ...prev,
        turn_state: 'TURN_ENDED'
      } : null);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-wof-blue mx-auto mb-4"></div>
          <p className="text-lg text-gray-600">Loading game...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg p-8 shadow-lg max-w-md">
          <div className="text-center">
            <div className="text-red-500 text-4xl mb-4">⚠️</div>
            <h2 className="text-xl font-bold text-gray-800 mb-2">Game Error</h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <button 
              onClick={() => window.location.reload()} 
              className="btn-primary"
            >
              Reload Game
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!gameStatus) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg p-8 shadow-lg max-w-md">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-wof-blue mb-4">🎡 Wheel of Fortune</h1>
            <p className="text-gray-600 mb-6">No active game found.</p>
            <p className="text-sm text-gray-500">
              Make sure your backend is running and create a game first.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-wof-blue mb-2">🎡 Wheel of Fortune</h1>
          <p className="text-lg text-gray-600">
            Round {gameStatus.current_round} of {gameStatus.total_rounds}
          </p>
          <p className="text-sm text-gray-500 capitalize">
            {gameStatus.game_state.replace('_', ' ').toLowerCase()} • {gameStatus.turn_state.replace('_', ' ').toLowerCase()}
          </p>
        </div>

        {/* Team Display */}
        <TeamDisplay teams={gameStatus.teams} />

        {/* Main Puzzle Area */}
        {gameStatus.current_puzzle && (
          <div className="bg-white rounded-lg shadow-lg mb-8">
            <PuzzleDisplay 
              puzzle={gameStatus.current_puzzle} 
              newlyRevealedLetters={newlyRevealedLetters}
            />
          </div>
        )}

        {/* Game Controls */}
        {gameStatus.game_state === 'IN_PROGRESS' && (
          <GameControls
            gameStatus={gameStatus}
            onSpin={handleSpin}
            onGuessLetter={handleGuessLetter}
            onSolve={handleSolve}
          />
        )}

        {/* Game Status Info */}
        <div className="bg-white rounded-lg p-4 shadow-sm mt-6">
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-600">
              <span className="font-medium">Game State:</span> {gameStatus.game_state.replace('_', ' ')}
            </div>
            <div className="text-sm text-gray-600">
              <span className="font-medium">Turn State:</span> {gameStatus.turn_state.replace('_', ' ')}
            </div>
            {gameStatus.last_wheel_result && (
              <div className="text-sm text-gray-600">
                <span className="font-medium">Last Spin:</span> {gameStatus.last_wheel_result}
              </div>
            )}
          </div>
          
          {/* Demo Notice */}
          <div className="mt-3 pt-3 border-t border-gray-200">
            <p className="text-xs text-gray-500 text-center">
              ⚠️ Demo Mode: This is a frontend-only demonstration. Game actions are simulated locally.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}; 