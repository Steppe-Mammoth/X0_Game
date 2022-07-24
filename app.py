import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from logger import logger

from bot.data.config import Config
from bot.handlers.routers import private_router, private_db_router
from bot.middlewares.db import DbSessionMiddleware
from bot.utils.bot_utils.set_bot_commands import set_default_commands


class BotParam:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    bot = Bot(token=Config.bot_token, parse_mode="HTML")


async def main():
    dp = BotParam.dp
    bot = BotParam.bot

    _engine = create_async_engine(Config.postgres_dsn, future=True)
    _async_session = sessionmaker(bind=_engine, expire_on_commit=False, class_=AsyncSession)

    private_db_router.message.middleware(DbSessionMiddleware(_async_session))
    private_db_router.callback_query.middleware(DbSessionMiddleware(_async_session))

    private_router.message.filter(F.chat.type == 'private')
    private_db_router.message.filter(F.chat.type == 'private')

    dp.include_router(router=private_router)
    dp.include_router(router=private_db_router)

    await set_default_commands(bot)

    try:
        logger.warning('Bot started')
        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        logger.warning('Bot close')


if __name__ == "__main__":
    asyncio.run(main())
