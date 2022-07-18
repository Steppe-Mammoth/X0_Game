from aiogram.dispatcher.filters.callback_data import CallbackData


class OpponentCB(CallbackData, prefix="opponent"):
    user_id: int
    count_rounds: int
