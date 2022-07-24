from typing import Optional, Generator, Sequence
from aiogram import Bot
from aiogram.types import InlineKeyboardButton

from text.game_text.stats.table_info import get_table_info_text, get_now_player_step_text, get_first_player_step_text, \
    get_present_players
from text.game_text.vote.retry_game import get_retry_game_vote_text, get_started_text_for_retry_game
from text.game_text.winners.exit_game import get_game_table_capitulated_text, get_game_capitulated_text

from text.game_text.winners.winners_party import get_winner_party_text
from text.utils.emoji import GetEmoji

from game.structure.message.data.dataclasses import MessageInfo, MessageVoteInfo
from game.structure.players.data.dataclasses import PlayerInfo
from game.structure.players.xo_winner import WinnerInfo
from game.structure.fields.data.dataclasses import TInfo

from bot.keyboards.field.field_keyboard import game_field_keyboard
from bot.keyboards.vote.retry_vote_keyboard import retry_vote_game_keyboard, retry_game_bot_keyboard


class MessageSender:
    @staticmethod
    async def notify_for_game_exit(bot: Bot, players: Sequence[PlayerInfo], player_exit: PlayerInfo):
        text = get_game_capitulated_text(player_exit)
        for player in players:
            await MessageTechnical.send_message(bot=bot, chat_id=player.id, text=text)


class MessageGameTable:
    @staticmethod
    async def _update_game_keyboard(bot: Bot, text: str, unique_message: MessageInfo, finish: bool, game_table: TInfo):
        keyboard = game_field_keyboard(table=game_table.table, unique_id=game_table.unique_id, finish=finish)
        await MessageTechnical.edit_message(bot, text=text, unique_message=unique_message, reply_markup=keyboard)

    @staticmethod
    async def send_game_table(bot: Bot, player_now: PlayerInfo, players: Sequence[PlayerInfo], game_table: TInfo):
        text = get_first_player_step_text(player_now)
        keyboard = game_field_keyboard(table=game_table.table, unique_id=game_table.unique_id)

        for user in players:
            user.msg_table = await MessageTechnical.send_message(bot=bot, chat_id=user.id, text=text,
                                                                 disable_notification=True, reply_markup=keyboard)

    @staticmethod
    async def _update_game_table(bot: Bot, text: str, players: Sequence[PlayerInfo], game_table: TInfo,
                                 finish: bool = False):
        keyboard = game_field_keyboard(table=game_table.table, unique_id=game_table.unique_id, finish=finish)

        for user in players:
            unique_message = user.msg_table
            await MessageTechnical.edit_message(bot, text=text, unique_message=unique_message, reply_markup=keyboard)

    @classmethod
    async def refresh_game_table(cls, bot: Bot,
                                 player_now: Optional[PlayerInfo], players: Sequence[PlayerInfo], game_table: TInfo):
        """Обновляется ход, изменяется текст обозначающих след ход"""

        text = get_now_player_step_text(player_now)
        await cls._update_game_table(bot=bot, text=text, players=players, game_table=game_table, finish=False)

    @classmethod
    async def finish_game_table(cls, bot: Bot,
                                players: Sequence[PlayerInfo], game_table: TInfo, winner: Optional[PlayerInfo] = None):
        """Ствится метка финиш на всех клетках + финишний текст"""

        text = get_winner_party_text(winner=winner)
        await cls._update_game_table(bot=bot, text=text, players=players, game_table=game_table, finish=True)

    @classmethod
    async def exit_game_table(cls, bot: Bot, players: Sequence[PlayerInfo], game_table: TInfo):
        text = get_game_table_capitulated_text()
        await cls._update_game_table(bot=bot, text=text, players=players, game_table=game_table, finish=True)


class MessageVote:

    @staticmethod
    async def delete_vote(bot: Bot, players: Sequence[PlayerInfo]):
        for player in players:
            await MessageTechnical.delete_message(bot=bot, unique_message=player.msg_vote)

    @classmethod
    async def send_vote_retry_game_for_players(cls, bot: Bot, players: Sequence[PlayerInfo]):
        keyboard = retry_vote_game_keyboard()
        text = get_started_text_for_retry_game()

        await cls.send_vote(bot=bot, players=players, text=text, keyboard=keyboard)

    @classmethod
    async def send_vote_retry_game_bot(cls, bot: Bot, players: Sequence[PlayerInfo]):
        keyboard = retry_game_bot_keyboard()
        text = get_present_players(players=players)

        await cls.send_vote(bot=bot, players=(players[0],), text=text, keyboard=keyboard)

    @staticmethod
    async def send_vote(bot: Bot, players: Sequence[PlayerInfo], text: str, keyboard):
        """Sending a message at the end of the game_text about the replay"""

        for user in players:
            msg = await MessageTechnical.send_message(bot=bot, chat_id=user.id,
                                                      text=text, disable_notification=True, reply_markup=keyboard)
            user.msg_vote = MessageVoteInfo(chat_id=msg.chat_id, message_id=msg.message_id)

    @staticmethod
    async def refresh_vote(bot: Bot, players: Sequence[PlayerInfo], confirm_count: int = 0, reply_markup: bool = False):

        text = get_retry_game_vote_text(players=players)
        keyboard = None

        if reply_markup:
            keyboard = retry_vote_game_keyboard(confirm_count=confirm_count)
        for user in players:
            await MessageTechnical.edit_message(bot=bot, text=text, unique_message=user.msg_vote, reply_markup=keyboard)


class MessageChat:
    def __init__(self):
        self.emoji_chat: Generator[str] = GetEmoji.symbols_chat_generator()

    @staticmethod
    async def pin_chat(bot: Bot, players: Sequence[PlayerInfo]):
        for player in players:
            await MessageTechnical.pin_message(bot=bot, unique_message=player.msg_chat, disable_notification=True)

    @staticmethod
    async def unpin_chat(bot: Bot, players: Sequence[PlayerInfo]):
        for player in players:
            await MessageTechnical.unpin_message(bot=bot, unique_message=player.msg_chat, disable_notification=True)

    @staticmethod
    async def send_chat(bot: Bot, players: Sequence[PlayerInfo]):
        text = '<b>GAME CHAT:</b> <tg-spoiler><i>SEND A MESSAGE</i></tg-spoiler>'

        for user in players:
            msg = await MessageTechnical.send_message(bot=bot, chat_id=user.id, text=text, disable_notification=True)
            user.msg_chat = msg

    async def edit_players_chat(self, bot: Bot, players: Sequence[PlayerInfo], message_text: str):
        emoji = next(self.emoji_chat)
        text = f'{emoji} {message_text}'

        for user in players:
            await MessageTechnical.edit_message(bot=bot, text=text, unique_message=user.msg_chat)


class MessageStat:

    @staticmethod
    async def send_stat(bot: Bot, players: Sequence[PlayerInfo], count_selected_games: int, count_games_played: int):
        """Sends a new statistics fields to each players and delete old stat"""
        text = get_table_info_text(players, count_selected_games, count_games_played=count_games_played)

        for user in players:
            await MessageTechnical.delete_message(bot=bot, unique_message=user.msg_stat)
            user.msg_stat = await MessageTechnical.send_message(bot=bot,
                                                                chat_id=user.id, text=text, disable_notification=True)

    @classmethod
    async def send_finish_stat(cls, bot: Bot, players: Sequence[PlayerInfo], win: WinnerInfo):
        finish_text = win.get_win_text()

        for user in players:
            await MessageTechnical.delete_message(bot=bot, unique_message=user.msg_stat)
            await bot.send_message(chat_id=user.id, text=finish_text)


class MessageTechnical:
    @staticmethod
    async def send_message(bot: Bot, chat_id: int, text: str, disable_notification: Optional[bool] = None,
                           reply_markup: Optional[InlineKeyboardButton] = None) -> MessageInfo:

        msg = await bot.send_message(chat_id=chat_id, text=text, disable_notification=disable_notification,
                                     reply_markup=reply_markup)

        return MessageInfo(chat_id=msg.chat.id, message_id=msg.message_id)

    @staticmethod
    async def edit_message(bot: Bot, text: str,
                           unique_message: MessageInfo, reply_markup: Optional[InlineKeyboardButton] = None):
        try:
            await bot.edit_message_text(text=text, chat_id=unique_message.chat_id, message_id=unique_message.message_id,
                                        reply_markup=reply_markup)
        except Exception as E:
            raise Exception(f'Message could not be edit: {unique_message} | {E}')

    @staticmethod
    async def delete_message(bot: Bot, unique_message: MessageInfo):
        if isinstance(unique_message, MessageInfo):
            try:
                await bot.delete_message(chat_id=unique_message.chat_id, message_id=unique_message.message_id)
            except Exception as E:
                raise Exception(f'Message could not be removed: {unique_message} | {E}')

    @staticmethod
    async def pin_message(bot: Bot, unique_message: MessageInfo, disable_notification: bool = True):
        try:
            await bot.pin_chat_message(chat_id=unique_message.chat_id, message_id=unique_message.message_id,
                                       disable_notification=disable_notification)
        except Exception as E:
            raise Exception(f'Message could not be pin: {unique_message} | {E}')

    @staticmethod
    async def unpin_message(bot: Bot, unique_message: MessageInfo, disable_notification: bool = True):
        try:
            await bot.pin_chat_message(chat_id=unique_message.chat_id, message_id=unique_message.message_id,
                                       disable_notification=disable_notification)
        except Exception as E:
            raise Exception(f'Message could not be unpin: {unique_message} | {E}')

    @staticmethod
    async def unpin_all_messages(bot: Bot, players: Sequence[PlayerInfo]):
        for player in players:
            await bot.unpin_all_chat_messages(chat_id=player.id)
