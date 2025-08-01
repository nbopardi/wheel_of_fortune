import React, { useState, useEffect } from 'react';
import type { GameStatus } from '../types/game';
import { useSounds } from '../hooks/useSounds';

interface GameControlsProps {
  gameStatus: GameStatus;
  onSpin?: () => void;
  onWheelSelect?: (value: number | string) => void;
  onGuessLetter?: (letter: string) => void;
  onSolve?: (solution: string) => void;
  onNextTeam?: () => void;
  onNextRound?: () => void;
}

// Helper function to convert turn state to human-readable text
const getTurnStateText = (turnState: string) => {
  const turnStateText = {
    'WAITING_FOR_SPIN': 'Ready to Spin',
    'WAITING_FOR_LETTER_GUESS': 'Choose a Letter',
    'WAITING_FOR_SOLVE_ATTEMPT': 'Ready to Solve',
    'TURN_ENDED': 'Turn Complete'
  }[turnState] || turnState;

  return turnStateText;
};

export const GameControls = ({ gameStatus, onSpin, onWheelSelect, onGuessLetter, onSolve, onNextTeam, onNextRound }: GameControlsProps) => {
  const [selectedLetter, setSelectedLetter] = useState('');
  const [solutionGuess, setSolutionGuess] = useState('');
  const [showSolveInput, setShowSolveInput] = useState(false);
  const [showWheelOptions, setShowWheelOptions] = useState(false);

  const { playSound, stopLoopingSounds } = useSounds();

  // Wheel values that can be selected
  const wheelValues = [100, 200, 300, 500, 750, 1000, 'BANKRUPT', 'LOSE A TURN', 'DANCE', 'STORY', 'WIN A CAR'];

  const { current_puzzle, turn_state, teams, game_state } = gameStatus;
  const currentTeam = teams.find(team => team.is_current_turn);

  // Play appropriate background sounds based on turn state and UI state
  useEffect(() => {
    if (turn_state === 'WAITING_FOR_SPIN' && game_state !== 'ROUND_COMPLETED') {
      // Play speedup sound when waiting for wheel spin (including when showing wheel options)
      playSound('speedup', { stopOthers: true });
    } else if (turn_state === 'WAITING_FOR_LETTER_GUESS') {
      // Play choose_letters sound when waiting for letter selection
      playSound('choose_letters', { stopOthers: true });
    } else {
      // Stop looping sounds for other states
      stopLoopingSounds();
    }
  }, [turn_state, showWheelOptions, game_state, playSound, stopLoopingSounds]);

  if (!current_puzzle || !currentTeam) {
    return null;
  }

  const canSpin = turn_state === 'WAITING_FOR_SPIN';
  const canGuessLetter = turn_state === 'WAITING_FOR_LETTER_GUESS';
  const canSolve = turn_state === 'WAITING_FOR_SOLVE_ATTEMPT' || turn_state === 'WAITING_FOR_LETTER_GUESS';
  const turnEnded = turn_state === 'TURN_ENDED';
  const roundCompleted = game_state === 'ROUND_COMPLETED';

  const handleShowWheelOptions = () => {
    setShowWheelOptions(true);
  };

  const handleWheelSelection = (value: number | string) => {
    if (onWheelSelect) {
      onWheelSelect(value);
    }
    setShowWheelOptions(false);
  };

  const handleLetterGuess = () => {
    if (onGuessLetter && selectedLetter && canGuessLetter) {
      // Stop choose_letters sound when letter is guessed
      stopLoopingSounds();
      
      onGuessLetter(selectedLetter);
      setSelectedLetter('');
    }
  };

  const handleSolveAttempt = () => {
    if (onSolve && solutionGuess.trim()) {
      // Stop any looping sounds when attempting to solve
      stopLoopingSounds();
      
      onSolve(solutionGuess.trim());
      setSolutionGuess('');
      setShowSolveInput(false);
    }
  };

  const handleNextTeam = () => {
    if (onNextTeam) {
      onNextTeam();
    }
  };

  const availableConsonants = current_puzzle.available_consonants || [];
  const availableVowels = current_puzzle.available_vowels || [];
  const vowelCost = 250;
  const canAffordVowels = currentTeam.current_round_money >= vowelCost;

  // Determine winners (for tie handling)
  const maxMoney = Math.max(...teams.map(team => team.total_money));
  const winners = teams.filter(team => team.total_money === maxMoney);
  const isTie = winners.length > 1;

  return (
    <div className="rounded-lg p-6 shadow-lg" style={{
      backgroundColor: 'rgba(255, 255, 255, 0.75)',
      backdropFilter: 'blur(10px)',
      border: '1px solid rgba(255, 255, 255, 0.2)'
    }}>
      <div className="text-center mb-6">
        {roundCompleted ? (
          <div>
            <h3 className="text-3xl font-bold text-yellow-600 mb-2">
              🏆 {isTie ? 'TIE!' : 'WINNER!'} 🏆
            </h3>
            {isTie ? (
              <div>
                <p className="text-xl font-bold text-wof-blue mb-2">
                  {winners.map(team => team.name).join(' & ')}
                </p>
                <p className="text-lg text-gray-700 mb-1">
                  Tied at ${maxMoney} each
                </p>
                <p className="text-sm text-gray-600">
                  What an amazing tie! All tied teams are winners!
                </p>
              </div>
            ) : (
              <div>
                <p className="text-xl font-bold text-wof-blue mb-2">
                  {currentTeam.name}
                </p>
                <p className="text-lg text-gray-700 mb-1">
                  Total Winnings: ${currentTeam.total_money}
                </p>
                <p className="text-sm text-gray-600">
                  Congratulations on solving the puzzle!
                </p>
              </div>
            )}
          </div>
        ) : (
          <div>
            <h3 className="text-xl font-bold text-wof-blue mb-2">
              {currentTeam.name}'s Turn
            </h3>
            <p className="text-gray-600 capitalize">
              {getTurnStateText(turn_state)}
            </p>
            <p className="text-sm text-gray-600 mt-1">
              Round Money: ${currentTeam.current_round_money} | Total: ${currentTeam.total_money}
            </p>
          </div>
        )}
        {gameStatus.last_wheel_result && !roundCompleted && (
          <div className="mt-2 px-4 py-2 bg-wof-gold bg-opacity-20 rounded-lg">
            <span className="font-bold text-wof-blue">
              Last Spin: {typeof gameStatus.last_wheel_result === 'number' ? `$${gameStatus.last_wheel_result}` : gameStatus.last_wheel_result}
            </span>
          </div>
        )}
      </div>

      {/* Round Completed - Show Final Standings */}
      {roundCompleted && (
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-800 mb-3 text-center">Final Standings</h4>
          <div className="space-y-2">
            {[...teams]
              .sort((a, b) => b.total_money - a.total_money)
              .map((team, index) => {
                const isWinner = team.total_money === maxMoney;
                const isTiedWinner = isTie && isWinner;
                
                return (
                  <div 
                    key={team.team_id} 
                    className={`flex justify-between items-center p-3 rounded-lg ${
                      isWinner 
                        ? isTiedWinner 
                          ? 'bg-yellow-100 border-2 border-yellow-400' 
                          : 'bg-yellow-100 border-2 border-yellow-400'
                        : 'bg-gray-100'
                    }`}
                  >
                    <div className="flex items-center">
                      <span className="text-lg font-bold mr-2">
                        {isWinner 
                          ? isTiedWinner 
                            ? '🤝' 
                            : '🥇'
                          : index === 1 || (isTie && winners.length > 1 && index === winners.length) 
                            ? '🥈' 
                            : index === 2 || (isTie && winners.length > 2 && index === winners.length + 1)
                              ? '🥉' 
                              : `${index + 1}.`
                        }
                      </span>
                      <span className={isWinner ? 'font-bold text-yellow-700' : 'font-medium'}>
                        {team.name}
                      </span>
                      {isTiedWinner && (
                        <span className="ml-2 text-xs bg-yellow-200 text-yellow-800 px-2 py-1 rounded-full">
                          TIED
                        </span>
                      )}
                    </div>
                    <span className={`font-bold ${isWinner ? 'text-yellow-700' : 'text-gray-700'}`}>
                      ${team.total_money}
                    </span>
                  </div>
                );
              })}
          </div>
          
          {/* Next Round or Game Complete Button */}
          <div className="text-center mt-6">
            {gameStatus.current_round < gameStatus.total_rounds ? (
              <button
                onClick={onNextRound}
                className="btn-primary text-lg px-8 py-3 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200"
              >
                Next Round ({gameStatus.current_round + 1}/{gameStatus.total_rounds}) →
              </button>
            ) : (
              <div className="space-y-3">
                <div className="text-2xl font-bold text-green-600">
                  🎊 GAME COMPLETE! 🎊
                </div>
                <p className="text-gray-600">
                  All {gameStatus.total_rounds} rounds completed!
                </p>
                <p className="text-sm text-gray-500">
                  Congratulations to all players!
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Turn Ended - Next Team Button */}
      {turnEnded && !roundCompleted && (
        <div className="text-center mb-6">
          <div className="mb-4 p-4 bg-gray-100 rounded-lg">
            <p className="text-gray-700 mb-2">Turn completed!</p>
            <p className="text-sm text-gray-600">
              {gameStatus.last_wheel_result === 'BANKRUPT' && 'Bankrupt! All round money lost.'}
              {gameStatus.last_wheel_result === 'LOSE A TURN' && 'Lose a turn! Moving to next team.'}
              {typeof gameStatus.last_wheel_result === 'number' && 'Letter guess was incorrect.'}
              {!gameStatus.last_wheel_result && 'Solve attempt was incorrect.'}
            </p>
          </div>
          <button
            onClick={handleNextTeam}
            className="btn-primary text-lg px-8 py-3 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200"
          >
            Next Team →
          </button>
        </div>
      )}

      {/* Spin Wheel Button / Wheel Selection */}
      {canSpin && !roundCompleted && (
        <div className="text-center mb-6">
          {!showWheelOptions ? (
            <button
              onClick={handleShowWheelOptions}
              className="btn-primary text-lg px-8 py-3 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
            >
              🎡 Spin the Wheel
            </button>
          ) : (
            <div className="space-y-4">
              <h4 className="font-semibold text-gray-800">Select your wheel result:</h4>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {wheelValues.map((value, index) => (
                  <button
                    key={index}
                    onClick={() => handleWheelSelection(value)}
                    className={`px-4 py-3 rounded-lg font-bold transition-all transform hover:scale-105 ${
                      typeof value === 'number'
                        ? 'bg-green-100 text-green-800 border-2 border-green-300 hover:bg-green-200'
                        : value === 'BANKRUPT'
                        ? 'bg-red-100 text-red-800 border-2 border-red-300 hover:bg-red-200'
                        : value === 'LOSE A TURN'
                        ? 'bg-orange-100 text-orange-800 border-2 border-orange-300 hover:bg-orange-200'
                        : value === 'DANCE'
                        ? 'bg-purple-100 text-purple-800 border-2 border-purple-300 hover:bg-purple-200'
                        : value === 'STORY'
                        ? 'bg-blue-100 text-blue-800 border-2 border-blue-300 hover:bg-blue-200'
                        : value === 'WIN A CAR'
                        ? 'bg-pink-100 text-pink-800 border-2 border-pink-300 hover:bg-pink-200'
                        : 'bg-yellow-100 text-yellow-800 border-2 border-yellow-300 hover:bg-yellow-200'
                    }`}
                  >
                    {typeof value === 'number' 
                      ? `$${value}` 
                      : value === 'DANCE'
                      ? '💃 DANCE ($1001)'
                      : value === 'STORY'
                      ? '📖 STORY ($1001)'
                      : value === 'WIN A CAR'
                      ? '🚗 WIN A CAR'
                      : value
                    }
                  </button>
                ))}
              </div>
              <button
                onClick={() => setShowWheelOptions(false)}
                className="text-sm text-gray-600 hover:text-gray-800 underline"
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      )}

      {/* Letter Guessing */}
      {canGuessLetter && !roundCompleted && (
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
                      : 'text-gray-800 border-gray-300 hover:border-wof-blue'
                  }`}
                  style={selectedLetter !== letter ? {
                    backgroundColor: 'rgba(255, 255, 255, 0.7)',
                    backdropFilter: 'blur(5px)'
                  } : undefined}
                >
                  {letter}
                </button>
              ))}
            </div>
          </div>

          {/* Vowels */}
          <div className="mb-4">
            <p className="text-sm text-gray-600 mb-2">
              Vowels (${vowelCost} each)
              {!canAffordVowels && (
                <span className="text-red-600 ml-2">- Insufficient funds</span>
              )}
            </p>
            <div className="flex flex-wrap gap-2">
              {availableVowels.map((letter) => (
                <button
                  key={letter}
                  onClick={() => canAffordVowels && setSelectedLetter(letter)}
                  disabled={!canAffordVowels}
                  className={`w-10 h-10 border-2 rounded font-bold transition-all ${
                    !canAffordVowels
                      ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed'
                      : selectedLetter === letter
                      ? 'bg-wof-gold text-white border-wof-gold'
                      : 'text-gray-800 border-gray-300 hover:border-wof-gold'
                  }`}
                  style={canAffordVowels && selectedLetter !== letter ? {
                    backgroundColor: 'rgba(255, 255, 255, 0.7)',
                    backdropFilter: 'blur(5px)'
                  } : undefined}
                >
                  {letter}
                </button>
              ))}
            </div>
            {!canAffordVowels && (
              <p className="text-xs text-gray-500 mt-1">
                You need at least ${vowelCost} to buy a vowel. Spin the wheel to earn money!
              </p>
            )}
          </div>

          {/* Guess Letter Button */}
          {selectedLetter && (
            <div className="text-center">
              <button
                onClick={handleLetterGuess}
                className="btn-secondary px-6 py-2 rounded-lg"
              >
                {['A', 'E', 'I', 'O', 'U'].includes(selectedLetter) 
                  ? `Buy "${selectedLetter}" for $${vowelCost}` 
                  : `Guess "${selectedLetter}"`
                }
              </button>
            </div>
          )}
        </div>
      )}

      {/* Solve Puzzle */}
      {canSolve && !roundCompleted && (
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
      {!roundCompleted && (
        <div className="mt-4 text-xs text-gray-500 text-center">
          {turn_state === 'WAITING_FOR_SPIN' && !showWheelOptions && 'Click "Spin the Wheel" to see your options after spinning your physical wheel'}
          {turn_state === 'WAITING_FOR_SPIN' && showWheelOptions && 'Select the result from your physical wheel spin'}
          {turn_state === 'WAITING_FOR_LETTER_GUESS' && 'Choose a letter to guess'}
          {turn_state === 'WAITING_FOR_SOLVE_ATTEMPT' && 'Try to solve the puzzle or guess another letter'}
          {turn_state === 'TURN_ENDED' && 'Click "Next Team" to continue with the next player'}
        </div>
      )}
    </div>
  );
}; 