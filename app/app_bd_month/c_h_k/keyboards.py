import sqlite3
import calendar
import datetime

from aiogram.types import InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

#from run_calendar import months_info, month_name_next




open_months = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Открыть Месяца', callback_data='open_months')],
])







# Текущий Календарь
async def current_calendar():
    keyboard = InlineKeyboardBuilder()


    conn = sqlite3.connect('months.sql')  # БД
    cur = conn.cursor()  # Курсор

    # Создаём новую таблицу в БД с пользователями
    cur.execute('SELECT * '
                'FROM months')
    # SELECT * - выбираем все паля
    #          FROM users - из такой таблицы как (users)

    months_ = cur.fetchall()  # fetchall() - функция, вернут нам полностью все найденные записи

    # info = ''
    # for _ in months_:
    #     info += f'Номер месяца: {_[1]}, Месяц: {_[2]}, Год: {_[3]}, Количество дней в месяце: {_[4]}, Первый день недели: {_[5]}\n\n'



    # id	Номер месяца	Месяц	   Год     	Количество дней в месяце	Первый день недели
    # id	Month_number	Month	Year_month	   Number_days_month	      First_day_week
    for id_, Month_number, Month, Year_month, Number_days_month, First_day_week in months_:
        if Month == calendar.month_name[int(datetime.datetime.now().strftime("%m"))]:

            # Дни недели
            week_day_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

            # Кнопки перед 1
            buttons_calandar = [_ for _ in range(1, int(Number_days_month) + 1)]

            # Кнопки перед 1 днём месяца
            buttons_before_1 = []
            for _ in range(1, int(First_day_week)):
                buttons_before_1.append('.')

            list_buttons = week_day_names + buttons_before_1 + buttons_calandar

            # Кнопки после 28,29,30,31 дней месяца
            for _ in range(1, (35 - int(Number_days_month) + 1 - int(First_day_week) + 1)):
                list_buttons.append('.')

            # добавление кнопок переключения месяцев
            list_buttons.append('<')
            list_buttons.append(Month)
            list_buttons.append('>')

            for _ in list_buttons:
                keyboard.add(InlineKeyboardButton(text = str(_), callback_data = str(_)+'_'+Month))

            cur.close()  # Закрываем курсор,  close() - функция, которая закрывает соединение с БД
            conn.close()  # Закрываем само соединение,  close() - функция, которая закрывает соединение с БД

            return keyboard.adjust(7).as_markup()


    #
    #
    # for month_name, days, first_day in months_:
    #     if month_name == calendar.month_name[int(datetime.datetime.now().strftime("%m"))]:
    #
    #         week_day_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    #         month = month_name
    #
    #         list_kb = [_ for _ in range(1, int(days) + 1)]
    #
    #         res_02 = []
    #         for _ in range(1, int(first_day)):
    #             res_02.append('.')
    #
    #         list_kb = week_day_names + res_02 + list_kb
    #         for _ in range(1, (35 - int(days)+1 - int(first_day)+1)):
    #             list_kb.append('.')
    #         list_kb.append('<')
    #         list_kb.append(month)
    #         list_kb.append('>')
    #         for day in list_kb:
    #             keyboard.add(InlineKeyboardButton(text = str(day), callback_data = str(day)+'_'+month))
    #         return keyboard.adjust(7).as_markup()


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


