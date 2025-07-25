import React from 'react';
import { GameBoard } from './components/GameBoard';
import type { GameStatus } from './types/game';

// Sample data for testing the display
const sampleGameStatus: GameStatus = {
  game_id: "sample-game-123",
  game_state: "IN_PROGRESS",
  turn_state: "WAITING_FOR_SPIN",
  current_round: 2,
  total_rounds: 3,
  teams: [
    {
      team_id: "team-1",
      name: "Team Alpha",
      members: ["Alice", "Bob"],
      current_round_money: 1500,
      total_money: 4250,
      has_free_spin: true,
      is_current_turn: true
    },
    {
      team_id: "team-2", 
      name: "Team Beta",
      members: ["Charlie", "Diana"],
      current_round_money: 800,
      total_money: 3100,
      has_free_spin: false,
      is_current_turn: false
    },
    {
      team_id: "team-3",
      name: "Team Gamma", 
      members: ["Eve", "Frank", "Grace"],
      current_round_money: 0,
      total_money: 5750,
      has_free_spin: false,
      is_current_turn: false
    }
  ],
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

function App() {
  return <GameBoard gameStatus={sampleGameStatus} />;
}

export default App;
