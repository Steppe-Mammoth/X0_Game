from aiogram.dispatcher.filters.callback_data import CallbackData


class MessageExpand(CallbackData, prefix="expand_msg"):
    expand_msg: bool
