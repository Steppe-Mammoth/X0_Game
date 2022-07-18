from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.callbacks.invite_callback import Invite


def get_confirm_invite_keyboard(invite_link: str):
    keyboard = InlineKeyboardBuilder()
    accept = InlineKeyboardButton(text='ACCEPT 🫂',
                                  callback_data=Invite(invite_link=invite_link, choice=True).pack())
    cancel = InlineKeyboardButton(text='CANCEL 👥',
                                  callback_data=Invite(invite_link=invite_link, choice=False).pack())

    keyboard.row(accept, cancel)
    return keyboard.as_markup()

