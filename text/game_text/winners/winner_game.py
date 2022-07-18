from typing import Sequence, Optional

from game.structure.base.data.dataclasses import GameStats
from game.structure.players.data.dataclasses import WinnerLoser, PlayerInfo


class WinnerText:

    @classmethod
    def get_text(cls, win: bool | WinnerLoser, players: Sequence[PlayerInfo], game_stats: GameStats) -> str:
        text: Optional[str] = None
        end_text = cls._get_game_info_text(game_stats=game_stats)

        if win is True:  # Буллевое значение для пометки ничьей
            text = cls._get_peace_text(players=players)

        elif isinstance(win, WinnerLoser):
            text = cls._get_winner_text(win_info=win)

        return text + '\n' + end_text

    @classmethod
    def _get_peace_text(cls, players: Sequence[PlayerInfo]) -> str:
        p1 = players[0]
        p2 = players[1]

        text = f'''
🕊 🕊 <b>ABSOLUTE PEACE</b> 🕊 🕊
| Losers:
 -  <b>{p1.name.split()[0].upper()}</b>: <b>{p1.count_winner}</b> wins
 -  <b>{p2.name.split()[0].upper()}</b>: <b>{p2.count_winner}</b> wins'''
        return text

    @classmethod
    def _get_winner_text(cls, win_info: WinnerLoser) -> str:
        winner = win_info.winner
        loser = win_info.loser

        text = f'''
Winner: * <b>{winner.name.split()[0].upper()}</b> | <b>{winner.count_winner}</b> wins
Loser:  * <b>{loser.name.split()[0].upper()}</b> | <b>{loser.count_winner}</b> wins'''
        return text

    @staticmethod
    def _get_game_info_text(game_stats: GameStats) -> str:
        text = f'''
Game info: 
    <tg-spoiler>* Peace🕊 : <b>{game_stats.count_peace}</b>
    * Playing games: <b>{game_stats.count_games_played}</b> / <b>{game_stats.count_selected_games}</b></tg-spoiler>'''
        return text
