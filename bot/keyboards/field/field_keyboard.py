from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.field_callback import Cell


def game_field_keyboard(table: list, unique_id: str = None, finish: bool = False):
    keyboard = InlineKeyboardBuilder()

    for index, cell_symbol in enumerate(table):
        used = False
        if cell_symbol in ('X', '0'):
            used = True

        cell_marker = '❎' if cell_symbol == 'X' else '🅾️' if cell_symbol == '0' else '⠀'
        cell_marker = '⠀' * 3 + cell_marker + '⠀' * 3

        btn_cell = InlineKeyboardButton(text=cell_marker, callback_data=Cell(symbol=cell_symbol,
                                                                             index_cell=index,
                                                                             used=used,
                                                                             finish=finish,
                                                                             unique_id=unique_id).pack())
        keyboard.row(btn_cell)

    keyboard.adjust(3)
    return keyboard.as_markup()
