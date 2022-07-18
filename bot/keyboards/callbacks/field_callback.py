from aiogram.dispatcher.filters.callback_data import CallbackData


class Cell(CallbackData, prefix="cell"):
    symbol: str | None
    index_cell: int

    used: bool
    """Param used - indicates that the cage is in use"""
    finish: bool
    """Param finish - charge of the end of the game_text"""
    unique_id: str | None
    """Unique id to avoid clicks from another game_text fields"""


