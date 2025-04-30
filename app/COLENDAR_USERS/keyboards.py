import calendar
import datetime

from aiogram.types import InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder


# Получаем текущий год
year = datetime.datetime.now().year

# Список для хранения информации о месяцах
months_info = []

# Проходим по всем месяцам от 1 до 12
for month_ in range(1, 13):
    # Получаем количество дней в месяце
    days_in_month = calendar.monthrange(year, month_)[1]

    # Получаем первый день недели для первого дня месяца (0 - понедельник, 6 - воскресенье)
    first_weekday = calendar.monthrange(year, month_)[0]

    # Преобразуем номер дня недели в строку
    weekday_names = [1, 2, 3, 4, 5, 6, 7]
    first_weekday_name = weekday_names [first_weekday]

    # Добавляем информацию о месяце в список
    months_info.append((calendar.month_name[month_], days_in_month, first_weekday_name))

# Текущий Календарь
async def current_calendar():
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
            print('>' + '_' + str(month))
            for day in res_01:
                keyboard.add(InlineKeyboardButton(text = str(day), callback_data = str(day)+'_'+month))
            return keyboard.adjust(7).as_markup()


# Следующий Календарь (>)
async def next_calendar():

    keyboard = InlineKeyboardBuilder()

    for month_name, days, first_day in months_info:
        if month_name == calendar.month_name[int(datetime.datetime.now().strftime("%m"))+1]:

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
            print('>' + '_' + str(month))
            for day in res_01:
                keyboard.add(InlineKeyboardButton(text = str(day), callback_data = str(day)+'_'+month))
            return keyboard.adjust(7).as_markup()


