import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.data import config
from bot.handlers.routers import private_router, private_db_router
from bot.middlewares.db import DbSessionMiddleware
from bot.utils.bot_utils.set_bot_commands import set_default_commands

logging.basicConfig(level=logging.INFO,
                    format=format('T: %(asctime)s | LVL: %(levelname)s | Func: %(funcName)s | L: '
                                  f'%(lineno)s | | MSG: %(message)s - %(name)s||\n{("-" * 150)}'),
                    datefmt='%H:%M:%S')

logger = logging.getLogger()


class BotParam:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")


async def main():
    dp = BotParam.dp
    bot = BotParam.bot

    _engine = create_async_engine(
        f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.IP}/{config.DB_NAME}",
        future=True)
    _async_session = sessionmaker(bind=_engine, expire_on_commit=False, class_=AsyncSession)

    private_db_router.message.middleware(DbSessionMiddleware(_async_session))
    private_db_router.callback_query.middleware(DbSessionMiddleware(_async_session))

    private_router.message.filter(F.chat.type == 'private')
    private_db_router.message.filter(F.chat.type == 'private')

    dp.include_router(router=private_router)
    dp.include_router(router=private_db_router)

    await set_default_commands(bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
