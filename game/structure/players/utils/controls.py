import random
from typing import Sequence, Optional

from game.structure.players.data.dataclasses import PlayerInfo


class PlayerManger:

    @staticmethod
    def get_next_player(player_now: Optional[PlayerInfo], players_sequence: Sequence[PlayerInfo]) -> PlayerInfo:
        """
        * Возвращает следующего игрока.
        Если player_now = None - возвращает первого игрока в списке"""

        p_now = player_now
        p1 = players_sequence[0]
        p2 = players_sequence[1]
        p_next = p2 if p_now == p1 else p1

        return p_next

    @staticmethod
    def get_player(user_id: int, players: Sequence[PlayerInfo]) -> Optional[PlayerInfo]:
        find_player = None

        for player in players:
            if user_id == player.id:
                find_player = player

        return find_player

    @staticmethod
    def shuffle_players(players_sequence: Sequence) -> list[PlayerInfo, PlayerInfo]:
        players_list = list(players_sequence)
        random.shuffle(players_list)
        return players_list
