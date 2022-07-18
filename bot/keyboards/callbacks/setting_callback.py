from aiogram.dispatcher.filters.callback_data import CallbackData


class SettingAccept(CallbackData, prefix='setting'):
    opponent_id: int
    count_rounds: int


