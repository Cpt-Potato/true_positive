import asyncio

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand

from bot.handlers import (
    FSMState,
    admin,
    admin_logout,
    help_info,
    send_screenshot,
    show_statistics,
    start,
)
from config import ADMIN_PASSWORD, bot, dp, logger
from db.base import create_table


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(
        start, Text(equals="Перезапуск", ignore_case=True), state="*"
    )
    dp.register_message_handler(help_info, commands="help", state="*")
    dp.register_message_handler(
        help_info, Text(equals="Помощь", ignore_case=True), state="*"
    )
    dp.register_message_handler(admin, Text(equals=ADMIN_PASSWORD), state="*")
    dp.register_message_handler(
        show_statistics,
        Text(equals="Статистика", ignore_case=True),
        state=FSMState.admin,
    )
    dp.register_message_handler(
        admin_logout, Text(equals="Выйти", ignore_case=True), state=FSMState.admin
    )
    dp.register_message_handler(
        send_screenshot, Text(contains="http", ignore_case=True), state="*"
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
