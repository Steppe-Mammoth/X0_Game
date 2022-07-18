from aiogram.dispatcher.filters.callback_data import CallbackData


class Invite(CallbackData, prefix="inviter"):
    invite_link: str
    choice: bool
