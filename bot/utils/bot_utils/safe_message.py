from contextlib import suppress

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError


async def safe_del_message(chat_id: int, message_id: int, bot: Bot, del_keyboard: bool = False) -> bool:
    """
    Safe deletion message, Optional keyboard

    :param del_keyboard: Delete keyboard if message has not been deleted
    :return: True if del message or keyboard is done | Else -> False"""
    deleted = False

    with suppress(TelegramAPIError):
        if await bot.delete_message(chat_id=chat_id, message_id=message_id):
            deleted = True

    if deleted is False and del_keyboard is True:
        with suppress(TelegramAPIError):
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)
            deleted = True

    return deleted
