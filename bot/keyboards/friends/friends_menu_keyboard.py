from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.callbacks.user_callback import OpponentCB
from data_base.commands.friends.friends_command import get_friends
from text.utils.emoji import GetEmoji


async def show_friends_keyboard(session: AsyncSession, user_id: int):
    friends = await get_friends(session, user_id=user_id)
    keyboard = InlineKeyboardBuilder()

    if friends is not None:
        emoji = GetEmoji.people(generator=True)

        for user in friends:
            friend_button = InlineKeyboardButton(text=f"{user.full_name} {next(emoji)}",
                                                 callback_data=OpponentCB(user_id=user.user_id,
                                                                          count_rounds=0).pack())
            keyboard.row(friend_button)
        keyboard.adjust(1)

    keyboard.row(InlineKeyboardButton(text='ADD FRIEND 👤',
                                      callback_data='add_friend'),
                 InlineKeyboardButton(text='🔙',
                                      callback_data='back_in_start_menu'))

    return keyboard.as_markup()
