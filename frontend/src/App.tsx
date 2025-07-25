import React, { useState } from 'react';
import { GameBoard } from './components/GameBoard';
import { GameSetup } from './components/GameSetup';
import type { GameStatus, Team } from './types/game';

function App() {
  const [gameStarted, setGameStarted] = useState(false);
  const [gameStatus, setGameStatus] = useState<GameStatus | null>(null);

  const handleStartGame = (teams: Team[], totalRounds: number) => {
    // Create a game status with the configured teams and rounds
    const newGameStatus: GameStatus = {
      game_id: `game-${Date.now()}`,
      game_state: "IN_PROGRESS",
      turn_state: "WAITING_FOR_SPIN",
      current_round: 1,
      total_rounds: totalRounds,
      teams: teams,
      current_puzzle: {
        solution: "THE QUICK BROWN FOX",
        category: "PHRASE",
        guessed_letters: ["T", "H", "E", "R", "S"],
        display: "THE _ _ _ _ _   _ R _ _ _   _ _ _",
        available_consonants: ["B", "C", "D", "F", "G", "J", "K", "L", "M", "N", "P", "Q", "V", "W", "X", "Y", "Z"],
        available_vowels: ["A", "I", "O", "U"]
      },
      last_wheel_result: 500
    };

    setGameStatus(newGameStatus);
    setGameStarted(true);
  };

  const handleNewGame = () => {
    setGameStarted(false);
    setGameStatus(null);
  };

  if (!gameStarted) {
    return <GameSetup onStartGame={handleStartGame} />;
  }

  return (
    <div>
      {/* New Game Button */}
      <div className="fixed top-4 left-4 z-10">
        <button
          onClick={handleNewGame}
          className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          ← New Game
        </button>
      </div>
      
      <GameBoard gameStatus={gameStatus} />
    </div>
  );
}

export default App;
