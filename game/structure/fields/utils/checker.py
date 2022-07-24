from typing import Sequence

from game.structure.fields.utils.technical import TableBase
from game.structure.players.data.dataclasses import PlayerInfo
from logger import logger


class TableChecker:
    _win_combinations = TableBase.get_win_combinations()

    @staticmethod
    def check_free_cells(count_steps: int, game_table: list):
        """:return: False if all cells used | True if cells free"""

        if count_steps / 2 == 5:
            if all(game_table):
                logger.info('ПРОВЕРКА КЛЕТОК: ВСЕ КЛЕТКИ ЗАНЯТЫ')
                return False
        else:
            return True

    @classmethod
    def get_this_party_winner(cls, count_steps: int, game_table: list,
                              players: Sequence[PlayerInfo]) -> PlayerInfo | None:
        if not count_steps / 2 >= 3:
            return

        table = game_table
        p_1 = players[0]
        p_2 = players[1]

        for row in cls._win_combinations:
            if table[row[0]] == table[row[1]] == table[row[2]] in (p_1.symbol, p_2.symbol):
                if table[row[0]] == p_1.symbol:
                    return p_1
                else:
                    return p_2

        return None
