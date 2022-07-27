from aiogram import Bot, types
from aiogram.dispatcher.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.menu.select_friends_keyboard import show_friends_keyboard, short_full_about_button
from bot.states.users.menu_states import Menu
from data_base.commands.friends.friends_command import add_friends, check_friends
from bot.utils.bot_utils.safe_message import safe_del_message
from data_base.commands.users.users_command import get_user
from logger import logger
from text.menu_text.friends.friends_menu import FriendsText


async def add_friend_to_bd(my_id: int, friend_id: int, bot: Bot, state: FSMContext, session: AsyncSession):
    """Added friend in bd and send notify for added users"""

    data = await state.get_data()
    msg = data.get('msg_menu')

    my_user = (await bot.get_chat_member(chat_id=my_id, user_id=my_id)).user
    friend_user = (await bot.get_chat_member(chat_id=friend_id, user_id=friend_id)).user

    text_for_me = FriendsText.notify_me_add_friend(friend_user.full_name)
    text_for_friend = FriendsText.notify_friend_add_friend(my_user.full_name)

    try:
        await add_friends(session=session, user1_id=my_id, user2_id=friend_id)
    except Exception as a:
        await bot.send_message(chat_id=my_user.id, text=FriendsText.error_added())
        logger.warn(f'ERROR. UNABLE TO ADD FRIEND | {my_id} - {friend_id}\n****{a}')
        return False

    if msg:
        await safe_del_message(msg[0], msg[1], bot=bot, del_keyboard=True)

    keyboard = await show_friends_keyboard(session, user_id=my_user.id, selected_id=friend_id)
    msg = await bot.send_message(chat_id=my_user.id, text=text_for_me, reply_markup=keyboard)

    await state.update_data(msg_menu=(msg.chat.id, msg.message_id))
    await bot.send_message(chat_id=friend_user.id, text=text_for_friend)


async def check_friend_in_bd(user_1_id: int, user_2_id: int,
                             bot: Bot, state: FSMContext, session: AsyncSession) -> bool:
    """
    Check friends and send me notify to if users is already friends

    :returns: True if users are not friends | False if users is already friends or friends not find in DB
    """

    data = await state.get_data()
    msg = data.get('msg_menu')

    friend_user = (await bot.get_chat_member(chat_id=user_2_id, user_id=user_2_id)).user

    if await get_user(session, user_id=user_2_id) is None:
        text_error = FriendsText.fail_add_friend()
        keyboard = short_full_about_button(expand_message=True)

    elif await check_friends(session, user1_id=user_1_id, user2_id=user_2_id):
        text_error = FriendsText.already_friends(friend_user.full_name)
        keyboard = await show_friends_keyboard(session, user_id=user_1_id, selected_id=friend_user.id)
        await state.set_state(Menu.navigate)

    else:
        return True  # Users not already friends

    if msg:
        await safe_del_message(msg[0], msg[1], bot=bot, del_keyboard=True)

    msg = await bot.send_message(chat_id=user_1_id, text=text_error, reply_markup=keyboard)
    await state.update_data(msg_menu=(msg.chat.id, msg.message_id))

    return False


async def add_users_to_friends(friend_id: int,
                               message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):
    my_user_id = message.from_user.id
    friend_user_id = friend_id

    if await check_friend_in_bd(my_user_id, friend_user_id, bot=bot, state=state, session=session) is False:
        return

    await add_friend_to_bd(my_user_id, friend_user_id, bot=bot, state=state, session=session)
    await state.set_state(Menu.navigate)
