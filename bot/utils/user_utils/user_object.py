from aiogram import Bot
from aiogram.types import User


async def get_user_object(user_id: int, bot: Bot) -> User:
    user = (await bot.get_chat_member(chat_id=user_id, user_id=user_id)).user
    return user
