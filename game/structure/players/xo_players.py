from typing import Optional, MutableSequence, Tuple

from game.structure.players.data.dataclasses import PlayerInfo
from game.structure.players.utils.controls import PlayerManger
from app import logger


class Players:
    def __init__(self, player_1: PlayerInfo, player_2: PlayerInfo):
        self.p1 = player_1
        self.p2 = player_2

        self._player_now: Optional[PlayerInfo] = None
        self._sequence: Optional[MutableSequence[PlayerInfo, PlayerInfo]] = None
        self._players_sequence_initialization()

    def get_now_player(self):
        return self._player_now

    def set_next_player(self):
        next_player = PlayerManger.get_next_player(player_now=self._player_now, players_sequence=self._sequence)
        self._player_now = next_player

    def reset_now_player(self):
        self._player_now = None

    def get_players(self) -> Tuple[PlayerInfo, PlayerInfo]:
        return self.p1, self.p2

    def get_player(self, user_id: int) -> Optional[PlayerInfo]:
        players = self.get_players()
        user = PlayerManger.get_player(user_id=user_id, players=players)
        return user

    def sequence_reverse(self):
        """
        * Реверсирует последовательность игроков [p1, p2] -> [p2, p1]
        * Сбрасует текущего игрока
        Задействуется в начале новой партии
        """
        self._sequence.reverse()
        self.reset_now_player()

        logger.info(f'REVERSE AND RESET - DONE')

    def _players_sequence_initialization(self):
        """
        * Создает начальный случайный порядок игроков на игру
        """
        players = self.get_players()
        self._sequence = PlayerManger.shuffle_players(players_sequence=players)
