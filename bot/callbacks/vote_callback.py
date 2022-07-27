from aiogram.dispatcher.filters.callback_data import CallbackData


class RetryGame(CallbackData, prefix='retry'):
    choice: bool
    confirm_count: int
