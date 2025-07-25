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

  const handleWheelSelect = (wheelResult: number | string) => {
    if (!gameStatus) return;

    // Handle BANKRUPT - reset current round money to 0
    if (wheelResult === 'BANKRUPT') {
      setGameStatus(prev => prev ? {
        ...prev,
        last_wheel_result: wheelResult,
        teams: prev.teams.map(team => 
          team.is_current_turn 
            ? { ...team, current_round_money: 0 }
            : team
        ),
        turn_state: 'TURN_ENDED'
      } : null);
    } else {
      setGameStatus(prev => prev ? {
        ...prev,
        last_wheel_result: wheelResult,
        turn_state: typeof wheelResult === 'number' ? 'WAITING_FOR_LETTER_GUESS' : 'TURN_ENDED'
      } : null);
    }
  };

  const handleNextTeam = () => {
    if (!gameStatus) return;

    const currentTeamIndex = gameStatus.teams.findIndex(team => team.is_current_turn);
    const nextTeamIndex = (currentTeamIndex + 1) % gameStatus.teams.length;

    setGameStatus(prev => prev ? {
      ...prev,
      teams: prev.teams.map((team, index) => ({
        ...team,
        is_current_turn: index === nextTeamIndex
      })),
      turn_state: 'WAITING_FOR_SPIN',
      last_wheel_result: undefined // Clear previous wheel result for new turn
    } : null);
  };

  const completeRound = () => {
    if (!gameStatus) return;

    // Transfer current round money to total money for all teams
    const updatedTeams = gameStatus.teams.map(team => ({
      ...team,
      total_money: team.total_money + team.current_round_money,
      current_round_money: 0 // Reset round money
    }));

    // Find the maximum total money
    const maxMoney = Math.max(...updatedTeams.map(team => team.total_money));
    
    // Find all teams with the maximum money (handles ties)
    const winners = updatedTeams.filter(team => team.total_money === maxMoney);
    
    // For display purposes, use the first winner (or solving team if they're tied for first)
    const solvingTeam = updatedTeams.find(team => team.is_current_turn);
    const primaryWinner = winners.includes(solvingTeam!) ? solvingTeam! : winners[0];

    // Reveal all letters
    const allLetters = gameStatus.current_puzzle.solution.split('').filter(char => char.match(/[A-Z]/i));
    
    setGameStatus(prev => prev ? {
      ...prev,
      current_puzzle: {
        ...prev.current_puzzle,
        guessed_letters: allLetters.map(l => l.toUpperCase())
      },
      teams: updatedTeams.map(team => ({
        ...team,
        is_current_turn: team.team_id === primaryWinner.team_id // Mark primary winner as current
      })),
      game_state: 'ROUND_COMPLETED' as const
    } : null);
  };

  const isPuzzleComplete = (solution: string, guessedLetters: string[]) => {
    // Get all unique letters from the solution (only alphabetic characters)
    const solutionLetters = [...new Set(
      solution.toUpperCase().split('').filter(char => char.match(/[A-Z]/))
    )];
    
    // Check if all solution letters have been guessed
    return solutionLetters.every(letter => guessedLetters.includes(letter));
  };

  const handleGuessLetter = (letter: string) => {
    if (!gameStatus || !gameStatus.current_puzzle) return;

    const puzzle = gameStatus.current_puzzle;
    const isCorrect = puzzle.solution.toUpperCase().includes(letter.toUpperCase());
    const currentTeam = gameStatus.teams.find(team => team.is_current_turn);
    
    if (!currentTeam) return;

    // Check if it's a vowel (costs $250)
    const isVowel = ['A', 'E', 'I', 'O', 'U'].includes(letter.toUpperCase());
    const vowelCost = 250;

    if (isCorrect) {
      // Count how many times the letter appears in the solution
      const letterCount = puzzle.solution.toUpperCase().split('').filter(char => char === letter.toUpperCase()).length;
      
      // Calculate money earned (consonants only, vowels are purchased)
      let moneyChange = 0;
      if (isVowel) {
        moneyChange = -vowelCost; // Deduct cost of vowel
      } else if (typeof gameStatus.last_wheel_result === 'number') {
        moneyChange = gameStatus.last_wheel_result * letterCount; // Earn money for consonants
      }

      // Create the new guessed letters array
      const newGuessedLetters = [...puzzle.guessed_letters, letter.toUpperCase()];

      // Check if puzzle is now complete
      const puzzleComplete = isPuzzleComplete(puzzle.solution, newGuessedLetters);

      // Add letter to guessed letters and show as newly revealed
      setNewlyRevealedLetters([letter.toUpperCase()]);
      
      setTimeout(() => {
        setNewlyRevealedLetters([]);
      }, 2000);

      if (puzzleComplete) {
        // Update the game state with the final letter, then complete the round
        setGameStatus(prev => prev ? {
          ...prev,
          current_puzzle: {
            ...prev.current_puzzle,
            guessed_letters: newGuessedLetters,
            available_consonants: prev.current_puzzle.available_consonants.filter(l => l !== letter.toUpperCase()),
            available_vowels: prev.current_puzzle.available_vowels.filter(l => l !== letter.toUpperCase())
          },
          teams: prev.teams.map(team => 
            team.is_current_turn 
              ? { 
                  ...team, 
                  current_round_money: Math.max(0, team.current_round_money + moneyChange)
                }
              : team
          )
        } : null);

        // Complete the round after a short delay to show the final letter
        setTimeout(() => {
          completeRound();
        }, 1000);
      } else {
        // Normal letter guess - continue playing
        setGameStatus(prev => prev ? {
          ...prev,
          current_puzzle: {
            ...prev.current_puzzle,
            guessed_letters: newGuessedLetters,
            available_consonants: prev.current_puzzle.available_consonants.filter(l => l !== letter.toUpperCase()),
            available_vowels: prev.current_puzzle.available_vowels.filter(l => l !== letter.toUpperCase())
          },
          teams: prev.teams.map(team => 
            team.is_current_turn 
              ? { 
                  ...team, 
                  current_round_money: Math.max(0, team.current_round_money + moneyChange)
                }
              : team
          ),
          turn_state: 'WAITING_FOR_SPIN' // Player continues
        } : null);
      }
    } else {
      // Letter not in puzzle - still deduct vowel cost if applicable, then end turn
      let moneyChange = 0;
      if (isVowel) {
        moneyChange = -vowelCost; // Still pay for vowel even if incorrect
      }

      setGameStatus(prev => prev ? {
        ...prev,
        current_puzzle: {
          ...prev.current_puzzle,
          available_consonants: prev.current_puzzle.available_consonants.filter(l => l !== letter.toUpperCase()),
          available_vowels: prev.current_puzzle.available_vowels.filter(l => l !== letter.toUpperCase())
        },
        teams: prev.teams.map(team => 
          team.is_current_turn 
            ? { 
                ...team, 
                current_round_money: Math.max(0, team.current_round_money + moneyChange)
              }
            : team
        ),
        turn_state: 'TURN_ENDED'
      } : null);
    }
  };

  const handleSolve = (solution: string) => {
    if (!gameStatus || !gameStatus.current_puzzle) return;

    const isCorrect = solution.toUpperCase() === gameStatus.current_puzzle.solution.toUpperCase();

    if (isCorrect) {
      completeRound();
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
        {(gameStatus.game_state === 'IN_PROGRESS' || gameStatus.game_state === 'ROUND_COMPLETED') && (
          <GameControls
            gameStatus={gameStatus}
            onWheelSelect={handleWheelSelect}
            onNextTeam={handleNextTeam}
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
                <span className="font-medium">Last Spin:</span> {typeof gameStatus.last_wheel_result === 'number' ? `$${gameStatus.last_wheel_result}` : gameStatus.last_wheel_result}
              </div>
            )}
          </div>
          
          {/* Demo Notice */}
          <div className="mt-3 pt-3 border-t border-gray-200">
            <p className="text-xs text-gray-500 text-center">
              ⚠️ Demo Mode: Spin your physical wheel, then select the result in the game to continue.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}; 