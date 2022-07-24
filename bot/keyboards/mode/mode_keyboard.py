from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from text.utils.emoji import GetEmoji


def get_game_mode_keyboard():
    people = GetEmoji.people(count=1)
    robot = GetEmoji.robot(count=1)

    keyboard = InlineKeyboardBuilder()
    user_vs_bot = InlineKeyboardButton(text=f'VS BOT {robot[0]}',
                                       callback_data='user_vs_bot')
    user_vs_user = InlineKeyboardButton(text=f'VS PLAYER {people[0]}',
                                        callback_data='user_vs_user')

    keyboard.row(user_vs_bot, user_vs_user)
    return keyboard.as_markup()
