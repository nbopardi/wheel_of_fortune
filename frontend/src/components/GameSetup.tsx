import React, { useState } from 'react';
import type { Team } from '../types/game';

interface GameSetupProps {
  onStartGame: (teams: Team[], totalRounds: number) => void;
}

export const GameSetup = ({ onStartGame }: GameSetupProps) => {
  const [numTeams, setNumTeams] = useState(3);
  const [totalRounds, setTotalRounds] = useState(3);
  const [teams, setTeams] = useState<Array<{name: string; members: string}>>([
    { name: 'Team Alpha', members: 'Alice, Bob' },
    { name: 'Team Beta', members: 'Charlie, Diana' },
    { name: 'Team Gamma', members: 'Eve, Frank' }
  ]);

  const handleNumTeamsChange = (newNum: number) => {
    setNumTeams(newNum);
    
    if (newNum > teams.length) {
      // Add new teams
      const newTeams = [...teams];
      for (let i = teams.length; i < newNum; i++) {
        newTeams.push({
          name: `Team ${String.fromCharCode(65 + i)}`, // Team A, Team B, etc.
          members: 'Player 1, Player 2'
        });
      }
      setTeams(newTeams);
    } else if (newNum < teams.length) {
      // Remove excess teams
      setTeams(teams.slice(0, newNum));
    }
  };

  const handleTeamChange = (index: number, field: 'name' | 'members', value: string) => {
    const updatedTeams = [...teams];
    updatedTeams[index] = { ...updatedTeams[index], [field]: value };
    setTeams(updatedTeams);
  };

  const handleStartGame = () => {
    // Convert setup data to Team objects
    const gameTeams: Team[] = teams.map((team, index) => ({
      team_id: `team-${index + 1}`,
      name: team.name.trim() || `Team ${index + 1}`,
      members: team.members.split(',').map(m => m.trim()).filter(m => m.length > 0),
      current_round_money: 0,
      total_money: 0,
      has_free_spin: false,
      is_current_turn: index === 0 // First team starts
    }));

    onStartGame(gameTeams, totalRounds);
  };

  const isValidSetup = () => {
    return teams.every(team => team.name.trim().length > 0) && 
           teams.length >= 2 && 
           teams.length <= 6 &&
           totalRounds >= 1 && 
           totalRounds <= 5;
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl w-full mx-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-wof-blue mb-2">🎡 Wheel of Fortune</h1>
          <p className="text-lg text-gray-600">Game Setup</p>
        </div>

        {/* Game Configuration Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Number of Teams */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Teams (2-6)
            </label>
            <div className="flex gap-2 flex-wrap">
              {[2, 3, 4, 5, 6].map(num => (
                <button
                  key={num}
                  onClick={() => handleNumTeamsChange(num)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    numTeams === num
                      ? 'bg-wof-blue text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {num}
                </button>
              ))}
            </div>
          </div>

          {/* Number of Rounds */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Rounds (1-5)
            </label>
            <div className="flex gap-2 flex-wrap">
              {[1, 2, 3, 4, 5].map(num => (
                <button
                  key={num}
                  onClick={() => setTotalRounds(num)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    totalRounds === num
                      ? 'bg-wof-blue text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {num}
                </button>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              {totalRounds === 1 ? 'Quick game' : totalRounds <= 3 ? 'Standard game' : 'Extended game'}
            </p>
          </div>
        </div>

        {/* Team Configuration */}
        <div className="mb-8">
          <h3 className="text-lg font-medium text-gray-800 mb-4">Configure Teams</h3>
          <div className="space-y-4">
            {teams.map((team, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Team Name
                    </label>
                    <input
                      type="text"
                      value={team.name}
                      onChange={(e) => handleTeamChange(index, 'name', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-wof-blue focus:border-transparent"
                      placeholder="Enter team name"
                      maxLength={30}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Team Members (comma-separated)
                    </label>
                    <input
                      type="text"
                      value={team.members}
                      onChange={(e) => handleTeamChange(index, 'members', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-wof-blue focus:border-transparent"
                      placeholder="Player 1, Player 2, ..."
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h4 className="font-medium text-blue-900 mb-2">📝 Setup Instructions</h4>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• Choose between 2-6 teams for your game</li>
            <li>• Select 1-5 rounds (3 rounds is standard)</li>
            <li>• Give each team a unique name</li>
            <li>• Add team members (optional but recommended)</li>
            <li>• The first team will start the game</li>
          </ul>
        </div>

        {/* Start Game Button */}
        <div className="text-center">
          <button
            onClick={handleStartGame}
            disabled={!isValidSetup()}
            className={`px-8 py-3 rounded-lg font-bold text-lg transition-colors ${
              isValidSetup()
                ? 'bg-wof-blue text-white hover:bg-blue-700'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            Start Game 🎯
          </button>
          {!isValidSetup() && (
            <p className="text-sm text-red-600 mt-2">
              Please ensure all teams have names and you have 2-6 teams.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}; 