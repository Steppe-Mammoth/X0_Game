from typing import Sequence, Optional

from game.structure.players.data.dataclasses import PlayerInfo
from app import logger


class GameChecker:

    @staticmethod
    def calculate_winners(count_selected_games: int,
                          count_games_played: int,
                          count_peace: int,
                          players: Sequence[PlayerInfo]) -> PlayerInfo | bool | None:

        winner: Optional[PlayerInfo] = None
        peace: Optional[bool] = None

        p1 = players[0]
        p2 = players[1]

        count_p1_wins = p1.count_winner
        count_p2_wins = p2.count_winner

        count_wins_to_win = (count_selected_games - count_peace) / 2

        if count_p1_wins > count_wins_to_win:
            winner = p1

        elif count_p2_wins > count_wins_to_win:
            winner = p2

        elif count_selected_games == count_games_played and count_p1_wins == count_p2_wins:
            peace = True

        if peace:
            return peace
        if winner:
            return winner

        logger.info(f'ВЫЧИСЛИТЬ ОСТАТОЧНУЮ ПОБЕДУ: PEACE: {peace} | WINNER: {winner}')


