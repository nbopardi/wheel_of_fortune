import React, { useState } from 'react';
import { GameBoard } from './components/GameBoard';
import { GameSetup } from './components/GameSetup';
import type { GameStatus, Team } from './types/game';
import { getInitialPuzzle, createPuzzle } from './utils/puzzles';

function App() {
  const [gameStarted, setGameStarted] = useState(false);
  const [gameStatus, setGameStatus] = useState<GameStatus | null>(null);

  const handleStartGame = (teams: Team[], totalRounds: number) => {
    // Get the initial puzzle from the puzzles data
    const initialPuzzleData = getInitialPuzzle();
    const initialPuzzle = createPuzzle(initialPuzzleData);

    // Create a game status with the configured teams and rounds
    const newGameStatus: GameStatus = {
      game_id: `game-${Date.now()}`,
      game_state: "IN_PROGRESS",
      turn_state: "WAITING_FOR_SPIN",
      current_round: 1,
      total_rounds: totalRounds,
      teams: teams,
      current_puzzle: initialPuzzle
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
          className="text-black px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105 cursor-pointer"
          style={{
            backgroundColor: 'rgba(229, 231, 235, 0.8)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.2)'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = 'rgba(229, 231, 235, 0.9)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'rgba(229, 231, 235, 0.8)';
          }}
        >
          ← New Game
        </button>
      </div>
      
      <GameBoard gameStatus={gameStatus} />
    </div>
  );
}

export default App;
