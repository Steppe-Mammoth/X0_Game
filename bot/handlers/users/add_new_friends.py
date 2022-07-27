from aiogram import types, Bot
from aiogram.dispatcher.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.messages_callback import MessageExpand
from bot.handlers.routers import private_router, private_db_router

from bot.keyboards.menu.select_friends_keyboard import short_full_about_button
from bot.states.users.menu_states import Menu
from bot.utils.bot_utils.safe_message import safe_del_message
from bot.utils.menu_utils.add_friends import add_users_to_friends

from text.menu_text.friends.friends_menu import FriendsText


@private_router.callback_query(MessageExpand.filter(), state=(Menu.navigate, Menu.send_contact))
async def expand_message(call: types.CallbackQuery, callback_data: MessageExpand, state: FSMContext, bot: Bot):
    await about_add_friend(call=call, state=state, bot=bot, callback_data=callback_data)


@private_router.callback_query(text='add_friend', state=Menu.navigate)
async def about_add_friend(call: types.CallbackQuery, state: FSMContext, bot: Bot, callback_data: MessageExpand = None):
    bot_obj = await bot.get_me()
    text_expand = FriendsText.add_friends(my_id=call.from_user.id, bot_username=bot_obj.username)

    if callback_data:
        text = text_expand.full if callback_data.expand_msg is True else text_expand.short
        choice_expand = False if callback_data.expand_msg is True else True
    else:
        text = text_expand.short
        choice_expand = True

    await state.set_state(Menu.send_contact)
    msg = await call.message.edit_text(text=text, reply_markup=short_full_about_button(expand_message=choice_expand))
    await state.update_data(msg_menu=(msg.chat.id, msg.message_id))


@private_db_router.message_handler(content_types=["contact", "text"], state=Menu.send_contact)
async def pre_add_users_to_friends(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):

    if message.contact:
        added_user_id = message.contact.user_id
    elif message.forward_from:
        added_user_id = message.forward_from.id
    else:
        data = await state.get_data()
        msg = data.get("msg_menu")
        error_text = FriendsText.get_error_format_msg()

        if msg:
            await safe_del_message(chat_id=msg[0], message_id=msg[1], bot=bot, del_keyboard=True)

        msg = await message.answer(text=error_text, reply_markup=short_full_about_button(expand_message=True))
        await state.update_data(msg_menu=(msg.chat.id, msg.message_id))
        return

    await add_users_to_friends(friend_id=added_user_id, message=message, state=state, bot=bot, session=session)


