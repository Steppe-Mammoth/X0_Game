from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.messages_callback import MessageExpand
from bot.callbacks.user_callback import OpponentCB
from data_base.commands.friends.friends_command import get_friends
from text.utils.emoji import GetEmoji


def short_full_about_button(expand_message: bool):
    text_for_full = "All methods"
    text_for_short = "Base method"
    text = text_for_full if expand_message is True else text_for_short

    keyboard = InlineKeyboardBuilder()

    button_expand = InlineKeyboardButton(text=text, callback_data=MessageExpand(expand_msg=expand_message).pack())
    button_back = InlineKeyboardButton(text='🔙', callback_data='back_in_friends_menu')

    keyboard.row(button_expand, button_back)
    return keyboard.as_markup()


async def show_friends_keyboard(session: AsyncSession, user_id: int, selected_id: int = None):
    """
    :param selected_id: Optional. if specified -> Found user will be marked in the list
    """

    friends = await get_friends(session, user_id=user_id)
    keyboard = InlineKeyboardBuilder()

    if friends is not None:
        emoji = GetEmoji.people(generator=True)

        for user in friends:
            text = f"{user.full_name} {next(emoji)}"

            if user.user_id == selected_id:
                text = "👉🏻 " + text

            friend_button = InlineKeyboardButton(text=text,
                                                 callback_data=OpponentCB(user_id=user.user_id, count_rounds=0).pack())
            keyboard.row(friend_button)
        keyboard.adjust(1)

    keyboard.row(InlineKeyboardButton(text='ADD FRIEND 👤',
                                      callback_data='add_friend'),
                 InlineKeyboardButton(text='🔙',
                                      callback_data='back_in_start_menu'))

    return keyboard.as_markup()
