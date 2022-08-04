from aiogram import types
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
from config import bot, logger
from db.models import Statistics
from db.services import get_statistics, write_to_db


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
    logger.info(f"Screenshot requested for {url}")
    user_id = message.from_user.id
    # send temp message
    loading = InputFile("./media/loading.png")
    msg = await bot.send_photo(
        chat_id=user_id,
        photo=loading,
        caption="Запрос принят. Получение скриншота...",
        reply_to_message_id=message.message_id,
    )
    try:
        url_domain, title, filename, result_time = await get_screenshot(user_id, url)
        file = InputMedia(
            media=InputFile(filename),
            caption=f"{title}, {url}, время обработки: {result_time:.2f} сек",
        )
    except Exception as e:
        logger.error(f"Something went wrong while taking screenshot, {e}")
        await msg.edit_caption("Что-то пошло не так. Попробуйте ещё раз позже.")
    # send statistics to db
    row = Statistics(user_id=user_id, url=url)
    await write_to_db(row)
    logger.info(f"Screenshot sent. {title}, {url}, {result_time:.2f} sec")
    # edit the message
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        f"Подробнее", url=f"https://www.whois.com/whois/{url_domain}"
    )
    keyboard.row(button)
    return await msg.edit_media(file, reply_markup=keyboard)


async def admin(message: types.Message):
    logger.info(f"Admin password entered, user_id = {message.from_user.id}")
    await message.answer(
        "Введён пароль администратора", reply_markup=get_admin_keyboard()
    )
    await FSMState.admin.set()


async def show_statistics(message: types.Message):
    logger.info(f"Statistics requested, user_id = {message.from_user.id}")
    statistics = await get_statistics()
    await message.answer(statistics)


async def admin_logout(message: types.Message):
    logger.info(f"Admin session finished, user_id = {message.from_user.id}")
    await message.answer(
        "Сессия администратора завершена", reply_markup=get_user_keyboard()
    )
    await FSMState.user.set()
