from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.callbacks.vote_callback import RetryGame


def retry_vote_game_keyboard(confirm_count: int = 0):
    keyboard = InlineKeyboardBuilder()

    confirm_button = InlineKeyboardButton(text=f'RETRY {confirm_count}/2',
                                          callback_data=RetryGame(choice=True, confirm_count=confirm_count + 1).pack())
    cancel_button = InlineKeyboardButton(text=f'EXIT',
                                         callback_data=RetryGame(choice=False, confirm_count=confirm_count).pack())

    keyboard.add(confirm_button, cancel_button)
    return keyboard.as_markup()


def retry_game_bot_keyboard():
    keyboard = InlineKeyboardBuilder()

    retry_button = InlineKeyboardButton(text=f'NEXT AI',
                                        callback_data="retry_game_bot")
    exit_button = InlineKeyboardButton(text=f'EXIT',
                                       callback_data="exit_in_menu")

    keyboard.add(retry_button, exit_button)
    return keyboard.as_markup()
