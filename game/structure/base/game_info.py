from typing import Optional

from game.structure.base.utils.checker import GameChecker
from game.structure.fields.utils.checker import TableChecker

from game.structure.players.xo_players import Players
from game.structure.players.data.dataclasses import PlayerInfo
from game.structure.base.data.dataclasses import GameStats
from game.structure.fields.table import TableInfo
from game.structure.players.xo_winner import WinnerInfo


class GameInfo:

    def __init__(self, player_1: PlayerInfo, player_2: PlayerInfo, count_games: Optional[int]):
        self.players = Players(player_1=player_1, player_2=player_2)
        self.stats = GameStats(count_selected_games=count_games)
        self.table = TableInfo()

    def check_free_cell(self) -> bool:
        """Возвращает False если все клетки заняты"""
        return TableChecker.check_free_cells(count_steps=self.table.count_steps, game_table=self.table.table)

    def check_party_winner(self) -> PlayerInfo | None:
        players = self.players.get_players()
        return TableChecker.get_this_party_winner(count_steps=self.table.count_steps, game_table=self.table.table,
                                                  players=players)

    def calculate_winners(self) -> Optional[WinnerInfo]:
        """Просчитывает подсчет для определения победителя всей игры"""
        count_games_played = self.stats.count_games_played
        count_selected_games = self.stats.count_selected_games
        count_peace = self.stats.count_peace

        if count_games_played < count_selected_games / 2:
            return

        players = self.players.get_players()
        winner = GameChecker.calculate_winners(count_selected_games=count_selected_games,
                                               count_games_played=count_games_played,
                                               count_peace=count_peace,
                                               players=players)

        if winner is not None:
            return WinnerInfo.instance_create(winner=winner, players=players, game_stat=self.stats)
