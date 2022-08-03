import os

from aiogram import Bot, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
    InputMedia,
)

from bot.keyboard import (
    get_admin_keyboard,
    get_user_keyboard,
    hello_message,
    help_message,
)
from bot.services import check_url, get_screenshot
from config import logger, bot
from db.models import Statistic
from db.services import get_statistic, write_to_db


class FSMState(StatesGroup):
    user = State()
    admin = State()


async def start(message: types.Message):
    await message.answer(text=hello_message, reply_markup=get_user_keyboard())


async def help_info(message: types.Message):
    await message.answer(help_message)


async def send_screenshot(message: types.Message):
    """Checks the url, sends temp dummy message, gets the screenshot
    and changes the temp message if everything went well"""
    url = message.text
    is_valid_url = await check_url(url)
    if not is_valid_url:
        return await message.answer(
            "Неверный адрес или сайт недоступен. "
            "Формат веб-сайта для ввода https://www.google.com"
        )
    user_id = message.from_user.id
    loading = InputFile("./media/loading.png")
    msg = await bot.send_photo(
        chat_id=user_id,
        photo=loading,
        caption="Запрос принят. Получение скриншота...",
        reply_to_message_id=message.message_id
    )
    title, filename, result_time = await get_screenshot(user_id, url)
    if os.path.exists(filename):
        file = InputMedia(
            media=InputFile(filename),
            caption=f"{title}, {url}, время обработки: {result_time:.2f} сек",
        )
        # send statistic to db
        row = Statistic(
            user_id=user_id,
            url=url
        )
        await write_to_db(row)
        logger.info(f"Скриншот отправлен. {title}, {url}, {result_time:.2f} сек")
        # edit the message
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(
            f"Подробнее", url=f"https://www.whois.com/whois/{url}"
        )
        keyboard.row(button)
        return await msg.edit_media(file, reply_markup=keyboard)
    return await message.answer("Что-то пошло не так. Попробуйте ещё раз.")


async def admin(message: types.Message):
    logger.info(f"Введён пароль администратора, user_id = {message.from_user.id}")
    await message.answer(
        "Введён пароль администратора", reply_markup=get_admin_keyboard()
    )
    await FSMState.admin.set()


async def show_statistic(message: types.Message):
    logger.info(f"Запрошена статистика, user_id = {message.from_user.id}")
    statistic = await get_statistic()
    await message.answer(statistic)


async def admin_logout(message: types.Message):
    await message.answer(
        "Сессия администратора завершена", reply_markup=get_user_keyboard()
    )
    await FSMState.user.set()
