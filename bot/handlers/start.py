from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from game.android.vs_bot_game import XOBot
from game.users.vs_user_game import XOUsers

from text.menu_text.started_menu.menu_text import MenuText

from bot.states.users.menu_states import Menu
from bot.handlers.routers import private_router, private_db_router
from bot.utils.inviter.invite_sender import Inviter
from bot.keyboards.mode.mode_keyboard import get_game_mode_keyboard

from data_base.commands.users.users_command import get_user, add_user


@private_db_router.message_handler(commands='start')
async def select_mode(message: types.Message, state: FSMContext, session: AsyncSession):
    user = message.from_user

    if await get_user(session, user_id=user.id) is None:
        await add_user(session, user=user)

    await msg_back_to_start_menu(message=message, state=state)


async def msg_back_to_start_menu(message: types.Message, state: FSMContext):
    await state.set_state(state=Menu.navigate)
    text = MenuText.start_menu(name_user=message.from_user.full_name)
    await message.answer(text=text, disable_notification=True, reply_markup=get_game_mode_keyboard())


@private_router.callback_query(text='back_in_start_menu', state=Menu.navigate)
async def call_back_to_start_menu(call: types.CallbackQuery):
    text = MenuText.start_menu(name_user=call.from_user.full_name)
    await call.message.edit_text(text=text, reply_markup=get_game_mode_keyboard())


@private_router.message_handler(commands='reboot', state='*')
async def emergency_reboot(message: types.Message, state: FSMContext):
    data = await state.get_data()
    game_user: XOUsers = data.get('game_player')
    game_bot: XOBot = data.get('bot_game')
    pre_inviter: Inviter = (await state.get_data()).get('inviter')

    if game_user is not None:
        p = game_user.g_info.players.get_player(message.from_user.id)
        await game_user.exit_game(p)

    if game_bot is not None:
        p = game_bot.g_info.players.get_player(message.from_user.id)
        await game_bot.exit_game(p)

    if pre_inviter is not None:
        pass

    await state.clear()
    await message.answer('<i><b>Emergency restart completed</b></i>'.upper())
