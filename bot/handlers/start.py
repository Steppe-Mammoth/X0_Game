import re
from aiogram import types, Bot
from aiogram.dispatcher.filters import CommandObject
from aiogram.dispatcher.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.utils.menu_utils.add_friends import add_users_to_friends
from bot.keyboards.menu.start_menu_keyboards import start_menu_button
from bot.utils.bot_utils.safe_message import safe_del_message
from game.android.vs_bot_game import XOBot
from game.users.vs_user_game import XOUsers

from text.menu_text.started_menu.menu_text import MenuText

from bot.states.users.menu_states import Menu
from bot.handlers.routers import private_router, private_db_router
from bot.utils.inviter.invite_sender import Inviter
from bot.keyboards.menu.select_mode_keyboard import get_game_mode_keyboard

from data_base.commands.users.users_command import get_user, add_user


async def start_menu(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    msg = data.get('msg_menu')
    text = MenuText.start_menu(name_user=message.from_user.full_name)

    if msg:
        await safe_del_message(chat_id=msg[0], message_id=msg[1], bot=bot, del_keyboard=True)

    await state.set_state(state=Menu.navigate)
    msg = await message.answer(text=text, disable_notification=True, reply_markup=get_game_mode_keyboard())

    await state.update_data(msg_menu=(msg.chat.id, msg.message_id))


@private_db_router.message_handler(commands='start', state=(None, Menu.navigate, Menu.send_contact))
async def select_mode(message: types.Message,
                      command: CommandObject, state: FSMContext, bot: Bot, session: AsyncSession):
    user = message.from_user
    ref_code = command.args

    if await get_user(session, user_id=user.id) is None:
        await add_user(session, user=user)

    if ref_code:
        id_ref = int(re.search(r"\d+", ref_code).group())
        await state.set_state(state=Menu.navigate)
        await add_users_to_friends(friend_id=id_ref, message=message, state=state, bot=bot, session=session)
        return

    await start_menu(message=message, state=state, bot=bot)


@private_router.callback_query(text='start_menu')
async def press_start_menu(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete_reply_markup()
    await start_menu(message=call.message, state=state, bot=bot)


@private_router.callback_query(text='back_in_start_menu', state=Menu.navigate)
async def call_back_to_start_menu(call: types.CallbackQuery):
    text = MenuText.start_menu(name_user=call.from_user.full_name)
    await call.message.edit_text(text=text, reply_markup=get_game_mode_keyboard())


@private_router.message_handler(commands='reboot', state='*')
async def emergency_reboot(message: types.Message, state: FSMContext):
    data = await state.get_data()
    game_user: XOUsers = data.get('game_player')
    game_bot: XOBot = data.get('bot_game')
    pre_inviter: Inviter = data.get('inviter')

    if game_user is not None:
        p = game_user.g_info.players.get_player(message.from_user.id)
        await game_user.exit_game(p)

    if game_bot is not None:
        p = game_bot.g_info.players.get_player(message.from_user.id)
        await game_bot.exit_game(p)

    if pre_inviter is not None:
        pass

    await state.clear()
    await message.answer('<i><b>Restart completed</b></i>'.upper(), reply_markup=start_menu_button())
