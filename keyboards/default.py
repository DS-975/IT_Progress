
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




def get_default_keyboard():
    button1 = KeyboardButton("Кнопка 1")
    button2 = KeyboardButton("Кнопка 2")
    return ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2)