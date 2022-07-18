from aiogram import types

from aiogram.dispatcher.dispatcher import Bot
from aiogram.types import BotCommandScopeAllPrivateChats


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(commands=[types.BotCommand(command="start", description="game start"),
                                        types.BotCommand(command="exit", description="Leave the game | capitulate🏳️"),
                                        types.BotCommand(command="reboot",
                                                         description="Emergency reboot for extreme cases")],
                              scope=BotCommandScopeAllPrivateChats(),
                              language_code=None)
