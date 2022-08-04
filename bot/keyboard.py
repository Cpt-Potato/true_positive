from aiogram import types

hello_message = (
    "Чтобы получить скриншот веб-сайта, напишите его в сообщении.\n"
    "Формат веб-сайта для ввода https://www.google.com"
)
help_message = (
    "Для перезапуска нажмите одноимённую кнопку или введите /start.\n"
    "Формат веб-сайта для ввода https://www.google.com"
)


def get_user_keyboard():
    buttons = ["Перезапуск", "Помощь"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def get_admin_keyboard():
    buttons = ["Статистика", "Выйти"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard
