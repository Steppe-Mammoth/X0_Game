from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.setting_callback import SettingAccept
from bot.callbacks.user_callback import OpponentCB


def get_confirm_setting_keyboard(user_id: int, count_rounds: int):
    keyboard = InlineKeyboardBuilder()
    accept = InlineKeyboardButton(text='ACCEPT ⭕',
                                  callback_data=SettingAccept(opponent_id=user_id, count_rounds=count_rounds).pack())
    cancel = InlineKeyboardButton(text='BACK ❌',
                                  callback_data=OpponentCB(user_id=user_id, count_rounds=0).pack())

    keyboard.row(accept, cancel)
    keyboard.adjust(2)
    return keyboard.as_markup()
