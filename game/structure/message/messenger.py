from typing import Optional, Sequence
from aiogram import Bot

from game.structure.base.data.dataclasses import GameStats
from game.structure.fields.data.dataclasses import TInfo
from game.structure.message.message_group import MessageChat, MessageStat, MessageGameTable, MessageVote, \
    MessageTechnical, MessageSender

from game.structure.players.data.dataclasses import PlayerInfo
from game.structure.players.xo_winner import WinnerInfo


class Messenger:
    _msg_stat = MessageStat
    _msg_table = MessageGameTable
    _msg_vote = MessageVote
    _msg_sender = MessageSender

    def __init__(self, bot: Bot):
        self._bot = bot
        self._msg_chat = MessageChat()

    async def chat_send(self, players: Sequence[PlayerInfo]):
        await self._msg_chat.send_chat(self._bot, players=players)
        await self._msg_chat.pin_chat(self._bot, players=players)

    async def chat_refresh(self, players: Sequence[PlayerInfo], message_text: str):
        await self._msg_chat.edit_players_chat(self._bot, players=players, message_text=message_text)

    async def chat_pin(self, players: Sequence[PlayerInfo]):
        await self._msg_chat.pin_chat(self._bot, players=players)

    async def chat_unpin(self, players: Sequence[PlayerInfo]):
        await self._msg_chat.unpin_chat(self._bot, players=players)

    async def table_send(self, player_now: PlayerInfo, players: Sequence[PlayerInfo], game_table: TInfo):
        await self._msg_table.send_game_table(self._bot, player_now=player_now, players=players, game_table=game_table)

    async def table_refresh(self, player_now: PlayerInfo, players: Sequence[PlayerInfo], game_table: TInfo):
        await self._msg_table.refresh_game_table(self._bot, player_now=player_now, players=players,
                                                 game_table=game_table)

    async def table_finish(self, players: Sequence[PlayerInfo],
                           game_table: TInfo, winner: Optional[PlayerInfo] = None):
        """
        Locks the game_text fields for further clicks
        :param game_table:
        :param players:
        :param winner: depending on the parameter will indicate the winner or indicate a draw
        """
        await self._msg_table.finish_game_table(self._bot, players=players, game_table=game_table, winner=winner)

    async def exit_table(self, players: Sequence[PlayerInfo], game_table: TInfo, exit_player: Optional[PlayerInfo]):
        await self._msg_table.exit_game_table(self._bot, players=players, game_table=game_table)
        await self._msg_sender.notify_for_game_exit(self._bot, players=players, player_exit=exit_player)

    async def vote_again_bot_game_send(self, players: Sequence[PlayerInfo]):
        await self._msg_vote.send_vote_retry_game_bot(self._bot, players=players)

    async def vote_again_game_players_send(self, players: Sequence[PlayerInfo]):
        await self._msg_vote.send_vote_retry_game_for_players(self._bot, players=players)

    async def vote_refresh(self, players: Sequence[PlayerInfo], confirm_count: int = 0, reply_markup: bool = False):
        await self._msg_vote.refresh_vote(self._bot, players=players, confirm_count=confirm_count,
                                          reply_markup=reply_markup)

    async def vote_delete(self, players: Sequence[PlayerInfo]):
        await self._msg_vote.delete_vote(self._bot, players=players)

    async def stat_send(self, players: Sequence[PlayerInfo], stats: GameStats):
        count_selected_games = stats.count_selected_games
        count_games_played = stats.count_games_played

        await self._msg_stat.send_stat(self._bot, players=players,
                                       count_selected_games=count_selected_games, count_games_played=count_games_played)

    async def stat_send_finish(self, players: Sequence[PlayerInfo], win: WinnerInfo):
        await self._msg_stat.send_finish_stat(self._bot, players=players, win=win)
        await self._msg_vote.send_vote_retry_game_for_players(self._bot, players=players)

    async def unpin_all_messages(self, players: Sequence[PlayerInfo]):
        await MessageTechnical.unpin_all_messages(self._bot, players=players)
