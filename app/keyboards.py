from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder



# Кнопки внизу
main_1 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог')],
    [KeyboardButton(text='Корзина'), KeyboardButton(text='Контакты')]
],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт ниже')



main_2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
    [InlineKeyboardButton(text='Корзина', callback_data='basket'),
     InlineKeyboardButton(text='Контакты', callback_data='contacts')]
])

# Кнопки вверху
settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Автор', url='https://t.me/danik_dizain')]
])


# Пример, если принимать и БД список и его выводить в кнопки
# from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

cars = ['1', 'Tesla', '2', 'Mercedes', '3', 'BMW', '4', 'Porsche', ]

async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(InlineKeyboardButton(text=car, url='https://t.me/danik_dizain'))
    return keyboard.adjust(2).as_markup()

# вызов этой функции await kb.inline_cars()
