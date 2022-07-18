from typing import Optional
from game.structure.players.data.dataclasses import PlayerInfo


def get_winner_party_text(winner: Optional[PlayerInfo] = None) -> str:
    if winner:
        text = f'<b>{winner.name} {winner.emoji} WINNER</b>'
    else:
        text = '<b>PEACE WINNER</b>'

    return text
