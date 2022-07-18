from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.callbacks.setting_callback import SettingAccept
from bot.keyboards.callbacks.user_callback import OpponentCB
from game.setting import RoundsSetting


def get_confirm_setting_keyboard(user_id: int, count_rounds: int):
    keyboard = InlineKeyboardBuilder()
    accept = InlineKeyboardButton(text='ACCEPT ⭕',
                                  callback_data=SettingAccept(opponent_id=user_id, count_rounds=count_rounds).pack())
    cancel = InlineKeyboardButton(text='BACK ❌',
                                  callback_data=OpponentCB(user_id=user_id, count_rounds=0).pack())

    keyboard.row(accept, cancel)
    keyboard.adjust(2)
    return keyboard.as_markup()


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
