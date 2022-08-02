import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand

from config import ADMIN_PASSWORD, TOKEN, logger
from db.base import create_table
from bot.handlers import (
    FSMState,
    admin,
    admin_logout,
    help_info,
    screenshot,
    show_statistic,
    start,
)

bot = Bot(token=TOKEN)  # , parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(
        start, Text(equals="Перезапуск", ignore_case=True), state="*"
    )
    dp.register_message_handler(help_info, Text(equals="Помощь", ignore_case=True))
    dp.register_message_handler(admin, Text(equals=ADMIN_PASSWORD), state="*")
    dp.register_message_handler(
        show_statistic,
        Text(equals="Статистика", ignore_case=True),
        state=FSMState.admin,
    )
    dp.register_message_handler(
        admin_logout, Text(equals="Выйти", ignore_case=True), state=FSMState.admin
    )
    dp.register_message_handler(
        screenshot, Text(contains="http", ignore_case=True), state="*"
    )


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Перезапуск"),
        BotCommand(command="/help", description="Помощь"),
    ]
    await bot.set_my_commands(commands)


async def main():
    await create_table()

    logger.info("Starting bot")

    register_handlers(dp)
    await set_commands(bot)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
