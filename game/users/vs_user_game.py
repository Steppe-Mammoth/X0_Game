from typing import Optional
from aiogram import Bot

from game.structure.base.game_info import GameInfo
from game.structure.base.data.dataclasses import GameParameters
from game.structure.base.utils.instance_creator import BaseCreator
from game.structure.message.messenger import Messenger
from game.structure.players.data.dataclasses import PlayerInfo

from logger import logger


class XOUsers:

    def __init__(self, parameters: GameParameters):
        self.started_parameters = parameters
        self.g_info: Optional[GameInfo] = None
        self.messenger: Optional[Messenger] = None

    async def new_game_initialization(self, bot: Bot):
        """
        * Создает новый образ игры
        * Создает игровой чат
        * Открепляет все сообщение"""

        self._initialization_game_info()
        self.messenger = Messenger(bot)

        players = self.g_info.players.get_players()

        await self.unpin_all_messages()
        await self.messenger.chat_send(players=players)

    async def reset_game_initialization(self, bot: Bot):
        """
        * Перезагружает новый игровой образ.
        Использовать при перезагрузке игры с теми же параметрами
        """
        await self.new_game_initialization(bot)

    async def start_new_party(self):
        """Выполняется только после инициализации base и messenger"""
        self.g_info.players.sequence_reverse()
        self.g_info.players.set_next_player()
        await self._send_game_table()

    async def next_game_step(self, index):
        self._edit_table(index=index)

        if await self._check_end_triggers_this_party():
            self.g_info.players.set_next_player()
            await self._table_refresh()

    async def chat_refresh(self, text):
        players = self.g_info.players.get_players()
        await self.messenger.chat_refresh(players=players, message_text=text)

    async def unpin_all_messages(self):
        players = self.g_info.players.get_players()
        await self.messenger.unpin_all_messages(players=players)

    async def _table_refresh(self):
        player_now = self.g_info.players.get_now_player()
        players = self.g_info.players.get_players()
        t_info = self.g_info.table.get_table_info()
        await self.messenger.table_refresh(player_now=player_now, players=players, game_table=t_info)

    def _edit_table(self, index):
        player_now = self.g_info.players.get_now_player()
        self.g_info.table.edit_table(index=index, symbol=player_now.symbol)

    def _initialization_game_info(self):
        self.g_info = BaseCreator.game_info_create(parameters=self.started_parameters)
        logger.info('initialization [game_text info] done'.upper())

    async def _send_game_table(self):
        self.g_info.table.new_table_initialization()

        player_now = self.g_info.players.get_now_player()
        players = self.g_info.players.get_players()
        g_stats = self.g_info.stats
        t_info = self.g_info.table.get_table_info()

        await self.messenger.stat_send(players=players, stats=g_stats)
        await self.messenger.table_send(players=players, game_table=t_info, player_now=player_now)

    async def _finish_party(self, peace: bool, winner: Optional[PlayerInfo]):
        players = self.g_info.players.get_players()
        t_info = self.g_info.table.get_table_info()

        await self.messenger.table_finish(players=players, game_table=t_info, winner=winner)

        self.g_info.stats.add_played_game(peace=peace)
        pre_win_game = self.g_info.calculate_winners()

        if pre_win_game:
            await self.messenger.stat_send_finish(players=players, win=pre_win_game)
        else:
            await self.start_new_party()

    async def _check_end_triggers_this_party(self) -> bool | None:
        """
        Checking use all cells and has winner and sender messages for end party

        :return: True if game_text not end
        """
        # copy
        free_cell = self.g_info.check_free_cell()
        get_winner = self.g_info.check_party_winner()

        if free_cell is True and get_winner is None:
            return True

        winner: Optional[PlayerInfo] = None
        peace: Optional[bool] = None

        if free_cell is False:
            peace = True

        if get_winner is not None:
            peace = False
            winner = get_winner
            winner.add_winner()

        await self._finish_party(peace=peace, winner=winner)

    async def exit_game(self, exit_player: PlayerInfo):
        players = self.g_info.players.get_players()
        t_info = self.g_info.table.get_table_info()

        await self.messenger.exit_table(players=players, game_table=t_info, exit_player=exit_player)
        await self.unpin_all_messages()

    def __del__(self):
        logger.warning(F"GAME PLAYER DELETED - DONE || {self}")
