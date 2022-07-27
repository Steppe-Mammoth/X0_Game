from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.routers import private_db_router
from bot.keyboards.menu.select_friends_keyboard import show_friends_keyboard
from bot.states.users.menu_states import Menu

from text.menu_text.started_menu.menu_text import MenuText


@private_db_router.callback_query(text='user_vs_user', state=Menu.navigate)
async def select_opponent(call: types.CallbackQuery, state: FSMContext, session: AsyncSession):

    text = MenuText.select_opponent()
    opponent_msg = await call.message.edit_text(text=text,
                                                reply_markup=await show_friends_keyboard(session,
                                                                                         user_id=call.from_user.id))
    await state.update_data(select_opponent_msg=opponent_msg.message_id)


@private_db_router.callback_query(text='back_in_friends_menu', state=(Menu.navigate, Menu.send_contact))
async def back_in_friends_menu(call: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.set_state(Menu.navigate)
    await select_opponent(call=call, state=state, session=session)
