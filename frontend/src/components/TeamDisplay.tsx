import type { Team } from '../types/game';

interface TeamDisplayProps {
  teams: Team[];
}

export const TeamDisplay = ({ teams }: TeamDisplayProps) => {
  return (
    <div className="rounded-lg p-4 shadow-sm mb-6" style={{
      backgroundColor: 'rgba(255, 255, 255, 0.75)',
      backdropFilter: 'blur(10px)',
      border: '1px solid rgba(255, 255, 255, 0.2)'
    }}>
      <h2 className="text-xl font-bold text-wof-blue mb-3">Teams</h2>
      <div className="space-y-2">
        {teams.map((team) => (
          <div 
            key={team.team_id} 
            className={`p-2 rounded ${
              team.is_current_turn 
                ? 'bg-wof-gold bg-opacity-20 border border-wof-gold' 
                : 'bg-gray-50'
            }`}
          >
            <div className="flex items-center justify-between">
              <div>
                <span className={`font-semibold ${
                  team.is_current_turn ? 'text-wof-blue' : 'text-gray-800'
                }`}>
                  {team.name}
                </span>
                <span className="text-sm text-gray-600 ml-2">
                  ({team.members.join(', ')})
                </span>
                {team.is_current_turn && (
                  <span className="ml-2 px-2 py-1 bg-wof-blue text-white text-xs rounded">
                    YOUR TURN
                  </span>
                )}
                {team.has_free_spin && (
                  <span className="ml-2 text-wof-gold">⭐</span>
                )}
              </div>
              <div className="text-right">
                <div className="text-sm text-gray-600">
                  Round: <span className="font-medium">${team.current_round_money.toLocaleString()}</span>
                </div>
                <div className="text-sm font-bold text-wof-blue">
                  Total: ${team.total_money.toLocaleString()}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}; 