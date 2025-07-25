export interface Team {
  team_id: string;
  name: string;
  members: string[];
  current_round_money: number;
  total_money: number;
  has_free_spin: boolean;
  is_current_turn: boolean;
}

export interface Puzzle {
  solution: string;
  category: string;
  guessed_letters: string[];
  display: string;
  available_consonants: string[];
  available_vowels: string[];
}

export interface GameStatus {
  game_id: string;
  game_state: 'SETUP' | 'IN_PROGRESS' | 'ROUND_COMPLETED' | 'GAME_COMPLETED';
  turn_state: 'WAITING_FOR_SPIN' | 'WAITING_FOR_LETTER_GUESS' | 'WAITING_FOR_SOLVE_ATTEMPT' | 'TURN_ENDED';
  current_round: number;
  total_rounds: number;
  teams: Team[];
  current_puzzle: Puzzle;
  last_wheel_result?: number | string;
}

export interface WheelResult {
  name: string;
  value: number | string;
}

export interface ApiResponse<T = any> {
  success: boolean;
  message?: string;
  error?: string;
  data?: T;
  game_status?: GameStatus;
}

export interface GameState {
  gameStatus: GameStatus | null;
  teams: Team[];
  currentPuzzle: Puzzle | null;
  isLoading: boolean;
  error: string | null;
} 