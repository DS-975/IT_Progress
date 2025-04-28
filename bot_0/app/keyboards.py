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

cars = ['1', 'Tesla', '2', 'Mercedes', '3', 'BMW', '4', 'Porsche']

async def inline_cars():
    keyboard = InlineKeyboardBuilder()

    for car in cars:

        keyboard.add(InlineKeyboardButton(text=car, callback_data = car))

    return keyboard.adjust(2).as_markup()

# вызов этой функции await kb.inline_cars()





# __________________________________________________________________________________


import calendar
import datetime

# Получаем текущий год
year = datetime.datetime.now().year

# Список для хранения информации о месяцах
months_info = []

# Проходим по всем месяцам от 1 до 12
for month in range(1, 13):
    # Получаем количество дней в месяце
    days_in_month = calendar.monthrange(year, month)[1]

    # Получаем первый день недели для первого дня месяца (0 - понедельник, 6 - воскресенье)
    first_weekday = calendar.monthrange(year, month)[0]

    # Преобразуем номер дня недели в строку
    weekday_names = [1, 2, 3, 4, 5, 6, 7]
    first_weekday_name = weekday_names [first_weekday]

    # Добавляем информацию о месяце в список
    months_info.append((calendar.month_name[month], days_in_month, first_weekday_name))



async def inline_calendar():
    keyboard = InlineKeyboardBuilder()

    for month_name, days, first_day in months_info:
        if month_name == calendar.month_name[int(datetime.datetime.now().strftime("%m"))]:

            weekday_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
            month = month_name

            res_01 = [_ for _ in range(1, int(days) + 1)]
            res_02 = []
            for _ in range(1, int(first_day)):
                res_02.append('.')

            res_01 = weekday_names + res_02 + res_01
            for _ in range(1, (35 - int(days)+1 - int(first_day)+1)):
                res_01.append('.')
            res_01.append('<')
            res_01.append(month)
            res_01.append('>')
            for day in res_01:
                keyboard.add(InlineKeyboardButton(text = str(day), callback_data = str(day)+'_'+month))
            return keyboard.adjust(7).as_markup()
