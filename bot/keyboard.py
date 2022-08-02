from aiogram import types

hello_message = "Чтобы получить скриншот веб-сайта, напишите его в сообщении"
help_message = "Для перезапуска нажмите одноимённую кнопку или введите /start"

start_buttons = ["Перезапуск", "Помощь"]
user_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
user_keyboard.add(*start_buttons)

buttons = ["Статистика", "Выйти"]
admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add(*buttons)
