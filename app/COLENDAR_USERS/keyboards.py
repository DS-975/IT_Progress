import calendar
import datetime

from aiogram.types import InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

from run_calendar import months_info, month_name_next

# Текущий Календарь
async def current_calendar():
    keyboard = InlineKeyboardBuilder()
    for month_name, days, first_day in months_info:
        if month_name == calendar.month_name[int(datetime.datetime.now().strftime("%m"))]:

            week_day_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
            month = month_name

            list_kb = [_ for _ in range(1, int(days) + 1)]
            res_02 = []
            for _ in range(1, int(first_day)):
                res_02.append('.')

            list_kb = week_day_names + res_02 + list_kb
            for _ in range(1, (35 - int(days)+1 - int(first_day)+1)):
                list_kb.append('.')
            list_kb.append('<')
            list_kb.append(month)
            list_kb.append('>')
            for day in list_kb:
                keyboard.add(InlineKeyboardButton(text = str(day), callback_data = str(day)+'_'+month))
            return keyboard.adjust(7).as_markup()


# Следующий Календарь (>)
async def next_calendar(next_month_name=None):

    global month_name_next

    keyboard = InlineKeyboardBuilder()

    default = int(datetime.datetime.now().strftime("%m"))
    default_next = default + 1




    for month_name, days, first_day in months_info:
        if month_name_next == calendar.month_name[default_next]:

            # week_day_names - дни недели
            week_day_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
            month = month_name_next

            # list_kb - Список для кнопок  
            list_kb = [_ for _ in range(1, int(days) + 1)]

            res_02 = []
            for _ in range(1, int(first_day)):
                res_02.append('.')

            list_kb = week_day_names + res_02 + list_kb
            if days == 30 and first_day == 7:
                for _ in range(1, 7):
                    list_kb.append('.')
            else:
                for _ in range(1, (35 - int(days) + 1 - int(first_day) + 1)):
                    list_kb.append('.')
            list_kb.append('<')
            list_kb.append(month)
            list_kb.append('>')

            month_name_next = str(month)

            for _ in list_kb:
                keyboard.add(InlineKeyboardButton(text = str(_), callback_data = str(_)+'_'+month))


            return keyboard.adjust(7).as_markup()


