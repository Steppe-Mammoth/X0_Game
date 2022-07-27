from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.user_callback import OpponentCB
from game.setting import RoundsSetting


def get_count_rounds_keyboard(user_id: int):
    keyboard = InlineKeyboardBuilder()
    for count in RoundsSetting.available_count_rounds:
        count_button = InlineKeyboardButton(text=f'{count}',
                                            callback_data=OpponentCB(user_id=user_id,
                                                                     count_rounds=count).pack())

        keyboard.add(count_button)

    keyboard.row(InlineKeyboardButton(text='🔙',
                                      callback_data='back_in_friends_menu'))
    return keyboard.as_markup()
