from aiogram import types, Bot
from aiogram.dispatcher.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.routers import private_router, private_db_router
from bot.handlers.start import msg_back_to_start_menu
from bot.keyboards.friends.friends_menu_keyboard import show_friends_keyboard
from bot.states.users.menu_states import Menu

from data_base.commands.users.users_command import get_user
from data_base.commands.friends.friends_command import check_friends, add_friends

from text.menu_text.friends.friends_menu import FriendsText
from logger import logger


@private_router.callback_query(text='add_friend', state=Menu.navigate)
async def start_add_friend(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Menu.send_contact)

    text = FriendsText.add_friends()
    msg = await call.message.edit_text(text=text)

    await state.update_data(add_friends=(msg.chat.id, msg.message_id))


@private_router.message_handler(commands='cancel', state=Menu.send_contact)
async def cancel_added_friend(message: types.Message, state: FSMContext):
    await msg_back_to_start_menu(message=message, state=state)


@private_db_router.message_handler(content_types=["contact", "text"], state=Menu.send_contact)
async def add_friend_contact_user(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):
    msg = (await state.get_data()).get('add_friends')
    user_id = message.from_user.id

    if message.contact:
        added_user_id = message.contact.user_id
    elif message.forward_from:
        added_user_id = message.forward_from.id
    else:
        text = FriendsText.get_error_format_msg()
        await message.answer(text=text)
        return

    check_friend = await check_friends(session, user_1=user_id, user_2=added_user_id)
    if check_friend is not None:  # Проверить есть ли юзер в списке друзей
        text = "THIS USER IS ALREADY ON THE FRIENDS LIST"

    else:
        added_user = await get_user(session, user_id=added_user_id)
        if added_user:
            name_friend: str = added_user.full_name
            text = FriendsText.added_friend(name_friend)

            await add_friends(session, my_user_id=message.from_user.id, friend_user_id=added_user.user_id)
        else:
            text = FriendsText.fail_add_friend()

    try:
        await bot.delete_message(chat_id=msg[0], message_id=msg[1])
    except Exception as e:
        logger.warning(e)

    await state.set_state(Menu.navigate)
    await message.answer(text=text, reply_markup=await show_friends_keyboard(session, user_id=message.from_user.id))
