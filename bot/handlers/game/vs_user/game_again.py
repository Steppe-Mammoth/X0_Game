from asyncio import sleep
from aiogram import types, F, Bot
from aiogram.dispatcher.fsm.context import FSMContext

from bot.handlers.routers import private_router
from bot.keyboards.callbacks.vote_callback import RetryGame
from bot.states.users.game_states import PlayerGame
from bot.utils.user_utils.user_fsm import set_user_fsm
from game.users.vs_user_game import XOUsers
from app import logger


@private_router.callback_query(RetryGame.filter(F.choice == False), state=PlayerGame.played)
async def cancel_retry_game_again(call: types.CallbackQuery, callback_data: RetryGame, state: FSMContext):
    data = await state.get_data()
    game: XOUsers = data.get('game_player')

    players = game.g_info.players.get_players()
    player = game.g_info.players.get_player(user_id=call.from_user.id)

    player.msg_vote.choice = callback_data.choice

    await game.messenger.vote_refresh(players=players, reply_markup=False)
    await game.unpin_all_messages()

    for player in players:
        await set_user_fsm(user_id=player.id, chat_id=player.id, state=state, clear=True)


@private_router.callback_query(RetryGame.filter(F.choice == True), state=PlayerGame.played)
async def vote_retry_game_again(call: types.CallbackQuery, callback_data: RetryGame, state: FSMContext, bot: Bot):
    data = await state.get_data()
    game: XOUsers = data.get('game_player')

    confirm_count = callback_data.confirm_count

    player = game.g_info.players.get_player(user_id=call.from_user.id)
    players = game.g_info.players.get_players()

    if player.msg_vote.choice is not None:
        await call.answer('Your vote has already been counted', show_alert=True)
        return

    player.msg_vote.choice = callback_data.choice

    try:
        await game.messenger.vote_refresh(players=players, confirm_count=confirm_count, reply_markup=True)
    except Exception as e:
        logger.warning(e)

    if all((players[0].msg_vote.choice, players[1].msg_vote.choice)):
        await sleep(2)

        try:
            await game.messenger.vote_delete(players=players)
        except Exception as a:
            logger.warning(a)
            return

        await game.reset_game_initialization(bot)
        await game.start_new_party()
