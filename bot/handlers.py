from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.keyboard import admin_keyboard, hello_message, help_message, user_keyboard
from bot.services import send_screenshot


class FSMState(StatesGroup):
    # user = State()
    getting_screenshot = State()
    admin = State()


async def start(message: types.Message):
    await message.answer(text=hello_message, reply_markup=user_keyboard)


async def help_info(message: types.Message):
    await message.answer(help_message)


async def screenshot(message: types.Message):
    await send_screenshot(message)


async def admin(message: types.Message):
    await message.answer("Введён пароль администратора", reply_markup=admin_keyboard)
    await FSMState.admin.set()


async def show_statistic(message: types.Message):
    # statistic = await get_statistic()
    # await message.answer(statistic)
    pass


async def admin_logout(message: types.Message):
    await message.answer("Сессия администратора завершена", reply_markup=user_keyboard)
    await FSMState.getting_screenshot.set()
