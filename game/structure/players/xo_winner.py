from typing import Sequence, Optional

from game.structure.base.data.dataclasses import GameStats
from text.game_text.winners.winner_game import WinnerText
from game.structure.players.utils.controls import PlayerManger

from game.structure.players.data.dataclasses import WinnerLoser, PlayerInfo


class WinnerInfo:
    def __init__(self, players: Sequence[PlayerInfo], game_stat: GameStats,
                 winner: Optional[PlayerInfo] = None, peace: Optional[bool] = None):
        """
        :param winner: optional if specified [peace]
        :param peace: optional if specified [winner]
        """
        self._peace = peace
        self._winner = winner

        self._loser: Optional[PlayerInfo] = None
        self._players = players
        self._game_stats = game_stat

        self._loser_detect()

    def _loser_detect(self):
        if self._winner:
            loser = PlayerManger.get_next_player(player_now=self._winner, players_sequence=self._players)
            self._loser = loser

    def get_winner(self) -> bool | WinnerLoser:
        if self._peace:
            return self._peace
        else:
            return WinnerLoser(winner=self._winner, loser=self._loser)

    def get_win_text(self) -> str:
        win = self.get_winner()
        return WinnerText.get_text(win=win, game_stats=self._game_stats, players=self._players)

    @staticmethod
    def instance_create(winner: PlayerInfo | bool, players: Sequence[PlayerInfo], game_stat: GameStats):
        return winner_create(winner=winner, players=players, game_stat=game_stat)


def winner_create(winner: PlayerInfo | bool, players: Sequence[PlayerInfo], game_stat: GameStats)\
        -> WinnerInfo:
    winner_info: Optional[WinnerInfo] = None

    if isinstance(winner, PlayerInfo):
        winner_info = WinnerInfo(winner=winner, players=players, game_stat=game_stat)

    if winner is True:
        winner_info = WinnerInfo(peace=True, players=players, game_stat=game_stat)

    return winner_info
