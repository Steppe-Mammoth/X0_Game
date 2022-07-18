from typing import Optional

from asyncio import sleep
from aiogram import Bot
from aiogram.types import User

from game.android.android_ai import BotAI
from game.structure.base.game_info import GameInfo
from game.structure.players.data.dataclasses import PlayerInfo
from game.structure.message.messenger import Messenger
from game.structure.players.utils.instance_create import bot_create_players_object
from app import logger


class XOBot:
    def __init__(self, user: User):
        self.user = user
        self.g_info: Optional[GameInfo] = None

        self.messenger: Optional[Messenger] = None
        self.AI: Optional[BotAI] = None

    async def new_game_initialization(self, bot: Bot):
        self._reset_game_initialization(bot)

        self.g_info.players.sequence_reverse()
        self.g_info.players.set_next_player()

        await self._send_game_table()

        if self.g_info.players.get_now_player() == self.g_info.players.p2:
            await self.step_for_bot()

    def _reset_game_initialization(self, bot: Bot):
        self._initialization_game_info()
        self.messenger = Messenger(bot)
        self.AI = BotAI(p1_symbols=self.g_info.players.p1.symbol, bot_symbols=self.g_info.players.p2.symbol)

    def _initialization_game_info(self):
        players = bot_create_players_object(user=self.user)
        self.g_info = GameInfo(player_1=players[0], player_2=players[1], count_games=None)

        logger.info('BOT initialization [game_text info] done'.upper())

    async def next_game_step(self, index):
        if self.g_info.players.get_now_player() == self.g_info.players.p1:
            self._edit_table(index=index)

            if await self._check_end_triggers_this_party():
                self.g_info.players.set_next_player()
                await self._table_refresh()
                await self.step_for_bot()

    async def _table_refresh(self):
        player_now = self.g_info.players.get_now_player()
        players = self.get_tuple_user()
        t_info = self.g_info.table.get_table_info()
        await self.messenger.table_refresh(player_now=player_now, players=players, game_table=t_info)

    async def step_for_bot(self):
        await sleep(1)
        table = self.g_info.table.get_table_info().table

        index = self.AI.selected_cell(table)
        self._edit_table(index=index)

        if await self._check_end_triggers_this_party():
            self.g_info.players.set_next_player()
            await self._table_refresh()

    async def _send_game_table(self):
        self.g_info.table.new_table_initialization()

        player_now = self.g_info.players.get_now_player()
        players = self.get_tuple_user()
        t_info = self.g_info.table.get_table_info()

        await self.messenger.table_send(players=players, game_table=t_info, player_now=player_now)

    async def _check_end_triggers_this_party(self) -> bool | None:
        """
        Checking use all cells and has winner and sender messages for end party

        :return: True if game_text not end
        """

        free_cell = self.g_info.check_free_cell()
        get_winner = self.g_info.check_party_winner()

        if free_cell is True and get_winner is None:
            return True

        winner: PlayerInfo | None = get_winner
        await self._finish_party(winner=winner)

    async def _finish_party(self, winner: Optional[PlayerInfo]):

        players = self.g_info.players.get_players()
        player = self.get_tuple_user()
        t_info = self.g_info.table.get_table_info()

        await self.messenger.table_finish(players=player, game_table=t_info, winner=winner)
        await self.messenger.vote_again_bot_game_send(players=players)

    def get_tuple_user(self):
        player = self.g_info.players.get_players()[0]
        return player,

    def _edit_table(self, index):
        player_now = self.g_info.players.get_now_player()
        self.g_info.table.edit_table(index=index, symbol=player_now.symbol)

    async def exit_game(self, exit_player: PlayerInfo):
        t_info = self.g_info.table.get_table_info()
        await self.messenger.exit_table(players=(exit_player,), game_table=t_info, exit_player=exit_player)

    def __del__(self):
        logger.warning(f'BOT GAME DELETED - DONE || {self}')
