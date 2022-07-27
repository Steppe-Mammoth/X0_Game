from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_menu_button():
    keyboard = InlineKeyboardBuilder()

    menu_button = InlineKeyboardButton(text='IN MENU',
                                       callback_data="start_menu")

    keyboard.add(menu_button)
    return keyboard.as_markup()
