import sqlite3
import calendar
import datetime

import app.app_bd_month.c_h_k.keyboards as kb

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()
router = Router()



# handlers
# Хэндлер на команду /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    conn = sqlite3.connect('months.sql') # БД
    cur = conn.cursor() # Курсор

    # Создаём новую таблицу в БД с пользователями
    cur.execute('CREATE TABLE '
                'IF NOT EXISTS months '
                '(id int auto_increment primary key,'
                'Month_number int varchar(2),'
                'Month varchar(15),'
                'Year_month int varchar(4),'
                'Number_days_month int varchar(3),'
                'First_day_week int varchar(3))') # метод execute позволяет выполнять SQL команды в БД
    # CREATE TABLE - создают таблицу
    # IF NOT EXISTS - если такой таблице ещё нет
    #               months - название таблице
    #
    # в () - указываем поля таблицы
    #   (id - идентификатор
    #       int - тип данных
    #           auto_increment - позволяет автоматически изменяться
    #                          primary key - первичный ключ
    #
    #    Month_number - Номер месяца
    #                 int - тип данных
    #                     varchar(2)  - длина этого полня 2 символа
    #    Month - Месяц
    #          varchar(15)  - длина этого полня 15 символов
    #
    #    Year_month - Год
    #               int - тип данных
    #                   varchar(4)  - длина этого полня 4 символа
    #
    #    Number_days_month - Количество дней в месяце
    #                      int - тип данных
    #                          varchar(3)  - длина этого полня 3 символа
    #
    #    First_day_week - Первый день недели
    #                   int - тип данных
    #                       varchar(3)  - длина этого полня 3 символа

    conn.commit() # commit() - функция, которая синхронизирует все изменения, в файле itproger.sql (БД)
    cur.close() # Закрываем курсор,  close() - функция, которая закрывает соединение с БД
    conn.close() # Закрываем само соединение,  close() - функция, которая закрывает соединение с БД
    await message.answer(f'Привет, {message.from_user.first_name} !\n',
                         reply_markup=kb.open_months)
    await months()




def drop_table_months():
    conn = sqlite3.connect('months.sql')  # БД
    cur = conn.cursor()  # Курсор

    # Удаляем таблицу months
    cur.execute('DROP TABLE months ')

    conn.commit()  # commit() - функция, которая синхронизирует все изменения, в файле itproger.sql (БД)
    cur.close()    # Закрываем курсор,  close() - функция, которая закрывает соединение с БД
    conn.close()   # Закрываем само соединение,  close() - функция, которая закрывает соединение с БД




# @run_once
is_months = False # переменная для единичного добавления данных в бд (months.sql)

async def months():
    global is_months
    if not is_months:
        # Список для хранения информации о месяцах
        months_info = []
        # [(1, 'January', 2025, 31, 3), (2, 'February', 2025, 28, 6), (3, 'March', 2025, 31, 6), (4, 'April', 2025, 30, 2), (5, 'May', 2025, 31, 4), (6, 'June', 2025, 30, 7), (7, 'July', 2025, 31, 2), (8, 'August', 2025, 31, 5), (9, 'September', 2025, 30, 1), (10, 'October', 2025, 31, 3), (11, 'November', 2025, 30, 6), (12, 'December', 2025, 31, 1)]

        # Номер месяца
        number_months = 0

        # Проходим по всем месяцам от 1 до 12
        for month_ in range(1, 13):
            # Номер месяца
            number_months += 1

            # Месяц
            months = calendar.month_name[month_]

            # Год
            year = datetime.datetime.now().year

            # Количество дней в месяце
            days_in_month = calendar.monthrange(year, month_)[1]

            # Первый день недели
            first_weekday_name = [1, 2, 3, 4, 5, 6, 7][calendar.monthrange(year, month_)[0]]

            # Добавляем информацию о месяце в список
            months_info.append((number_months, months, year, days_in_month, first_weekday_name))

        conn = sqlite3.connect('months.sql')  # БД
        cur = conn.cursor()  # Курсор

        for number_months, months, year, days_in_month, first_weekday_name in months_info:
            # Создаём новую таблицу в БД с пользователями
            cur.execute('INSERT INTO '
                        'months '
                        '(Month_number, '
                        'Month, '
                        'Year_month, '
                        'Number_days_month,'
                        'First_day_week) '
                        'VALUES '
                        '("%s","%s","%s","%s","%s")' % (number_months, months, year, days_in_month, first_weekday_name))

        conn.commit()  # commit() - функция, которая синхронизирует все изменения, в файле itproger.sql (БД)
        cur.close()  # Закрываем курсор,  close() - функция, которая закрывает соединение с БД
        conn.close()  # Закрываем само соединение,  close() - функция, которая закрывает соединение с БД
        #print("Функция выполняется впервые")
        is_months = True
    #else:
        #print("Функция уже вызывалась")








@router.callback_query(F.data == 'open_months')
async def next_m(callback_query: CallbackQuery):
    #Отправляем новое сообщение с кнопками
    await callback_query.message.answer('Текущий месяц',
                         reply_markup = await kb.current_calendar()) # Выскакивает комментарий в центре и сразу пропадает

    # Не забудьте ответить на колбэк, чтобы убрать "часики" у кнопки
    await callback_query.answer()














def open_months():
    conn = sqlite3.connect('months.sql')  # БД
    cur = conn.cursor()  # Курсор

    # Создаём новую таблицу в БД с пользователями
    cur.execute('SELECT * '
                'FROM months')
    # SELECT * - выбираем все паля
    #          FROM users - из такой таблицы как (users)

    months_ = cur.fetchall()  # fetchall() - функция, вернут нам полностью все найденные записи

    info = ''
    for _ in months_:
        info += f'Номер месяца: {_[1]}, Месяц: {_[2]}, Год: {_[3]}, Количество дней в месяце: {_[4]}, Первый день недели: {_[5]}\n\n'

    cur.close()  # Закрываем курсор,  close() - функция, которая закрывает соединение с БД
    conn.close()  # Закрываем само соединение,  close() - функция, которая закрывает соединение с БД
    return info









# _____________________________________________________



#
#
#
#
# # async def catalog(callback: CallbackQuery):
# #     await callback.answer('Вы выбрали следующий месяц',
# @router.callback_query(F.data == f'>_May')
# async def next_m(callback_query: CallbackQuery):
#
#     # Удаляем предыдущее сообщение (если оно есть)
#     await callback_query.message.delete()  # Удаляем сообщение, на которое нажали кнопку
#
#     # Отправляем новое сообщение с кнопками
#     await callback_query.message.answer('Вы выбрали следующий месяц',
#                          reply_markup = await kb.next_calendar()) # Выскакивает комментарий в центре и сразу пропадает
#
#     # Не забудьте ответить на колбэк, чтобы убрать "часики" у кнопки
#     await callback_query.answer()
#
# @router.callback_query(F.data == 'contacts')
# async def contacts(callback: CallbackQuery):
#     await callback.answer('Вы выбрали Контакты', show_alert=True) # Выскакивает комментарий в центре и ждёт когда нажмёте на OK
#     await callback.message.answer(f'Привет, вы нажали на - Контакты !') # Сообщение от бота под онлайн кнопками
#     #await callback.message.answer(f'Привет, вы нажали на - Каталог !') # Сообщение от бота под онлайн кнопками
#
# @router.message(Command("dice"))
# async def cmd_dice(message: Message):
#     await message.answer_dice(emoji="🎲")
#
# # Тест Хэндлеров
# # Хэндлер на команду /help
# @router.message(Command('help'))
# async def get_help(message: Message):
#     await message.answer('Список команд для этого бота\n'
#                          '\n'
#                          '/calendar - вывести календарь\n'
#                          '/dice - бросить кубик\n'
#                          '/help - просмотр команд\n'
#                          '/start - запуск бота\n')
#
# @router.message(Command('calendar'))
# async def send_calendar(message:Message):
#     await message.answer(text=f'Календарь на {calendar.month_name[int(datetime.datetime.now().strftime("%m"))]}  Выберите дату:',
#                          reply_markup = await kb.inline_calendar())
#
# @router.callback_query(F.data == '1')
# async def catalog(callback: CallbackQuery):
#     await callback.answer(f'Вы выбрали - 1')
#
#
