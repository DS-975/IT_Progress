
import logging
import asyncio
import sqlite3


from config import TOKEN


from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup

from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton, Message, CallbackQuery






# Инициализация бота и диспетчера
# Объект бота
bot = Bot(token=TOKEN)
name = None

# Диспетчер
storage = MemoryStorage()
dp = Dispatcher(storage=storage)




# Запуск процесса поллинга новых апдейтов
async def main():
    #dp.include_router(router)
    await dp.start_polling(bot)

# Определяем состояния
class Form(StatesGroup):
    name = State()
    password = State()

async def set_user_state(state: FSMContext, state_name: State):
    """Устанавливает состояние пользователя."""
    await state.set_state(state_name)




@dp.message(Command('start'))
async def start_0(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('../itproger.sql') # БД
    cur = conn.cursor() # Курсор

    # Создаём новую таблицу в БД с пользователями
    cur.execute('CREATE TABLE '
                'IF NOT EXISTS users '
                '(id int auto_increment primary key,'
                'name varchar(50),'
                'pass varchar(50))') # метод execute позволяет выполнять SQL команды в БД
    # CREATE TABLE - создают таблицу
    # IF NOT EXISTS - если такой таблице ещё нет
    # users - название таблице
    # в () - указываем поля таблицы
    #   (id - идентификатор
    #       int - тип данных
    #           auto_increment - позволяет автоматически изменяться
    #                          primary key - первичный ключ
    #   name - поля для имине пользователя
    #        varchar - тип данных
    #               (50) - длина этого полня 50 символов
    #   pass - поле которое хранит пароль пользователя
    #        varchar - тип данных
    #               (50) - длина этого полня 50 символов

    conn.commit() # commit() - функция, которая синхронизирует все изменения, в файле itproger.sql (БД)
    cur.close() # Закрываем курсор,  close() - функция, которая закрывает соединение с БД
    conn.close() # Закрываем само соединение,  close() - функция, которая закрывает соединение с БД

    await message.answer('Привет, сейчас тебя зарегистрируем!\n\nВведите ваше имя')

    # Устанавливаем состояние ожидания имени пользователя через вспомогательную функцию
    await set_user_state(state, Form.name)


@dp.message(Form.name)
async def user_name(message: types.Message, state: FSMContext):
    global name
    name = message.text # Получаем имя пользователя из сообщения


    await message.answer('Введите пароль')

    # Устанавливаем состояние ожидания имени пользователя через вспомогательную функцию
    await set_user_state(state, Form.password)


@dp.message(Form.password)
async def user_pass(message: types.Message, state: FSMContext):
    password = message.text  # Получаем имя пользователя из сообщения

    conn = sqlite3.connect('../itproger.sql')  # БД
    cur = conn.cursor()  # Курсор

    # Создаём новую таблицу в БД с пользователями
    cur.execute('INSERT INTO '
                'users '
                '(name, pass)'
                'VALUES'
                '("%s","%s")' % (name, password))  # метод execute позволяет выполнять SQL команды в БД
                # '("%s","%s")' % (name, password))  # метод execute позволяет выполнять SQL команды в БД
    # INSERT INTO - добавляем новую запись
    #             users - в такую таблицу (users)
    # в () - указываем поля таблицы
    #   (name - имя
    #          pass) - пароль
    #               VALUES -
    #                      (name,- подставляем по name
    #                             password) - подставляем под pass

    conn.commit()  # commit() - функция, которая синхронизирует все изменения, в файле itproger.sql (БД)
    cur.close()  # Закрываем курсор,  close() - функция, которая закрывает соединение с БД
    conn.close()  # Закрываем само соединение,  close() - функция, которая закрывает соединение с БД
    await add_user(message, state)



async def add_user(message: types.Message, state: FSMContext):
    await state.clear()  # Завершаем состояние
    await message.answer(f"Пользователь зарегистрирован!", reply_markup=markup)



# кнопки
markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Список пользователей', callback_data='users')]])


# меджек фильтр - F
@dp.callback_query(F.data == 'users')
async def how_are_you(callback: CallbackQuery):
    conn = sqlite3.connect('../itproger.sql')  # БД
    cur = conn.cursor()  # Курсор

    # Создаём новую таблицу в БД с пользователями
    cur.execute('SELECT * '
                'FROM users')
    # SELECT * - выбираем все паля
    #          FROM users - из такой таблицы как (users)

    users = cur.fetchall()  # fetchall() - функция, вернут нам полностью все найденные записи

    info = ''
    for _ in users:
        info += f'Имя: {_[1]}, пароль: {_[2]}\n'

    cur.close()  # Закрываем курсор,  close() - функция, которая закрывает соединение с БД
    conn.close()  # Закрываем само соединение,  close() - функция, которая закрывает соединение с БД

    await callback.message.answer(info) # Ответ на вопрос как дела, а не новое сообщение от бота


@dp.message(Command('users'))
async def get_help(message: Message):
    conn = sqlite3.connect('../itproger.sql')  # БД
    cur = conn.cursor()  # Курсор

    # Создаём новую таблицу в БД с пользователями
    cur.execute('SELECT * '
                'FROM users')
    # SELECT * - выбираем все паля
    #          FROM users - из такой таблицы как (users)

    users = cur.fetchall()  # fetchall() - функция, вернут нам полностью все найденные записи

    info = ''
    for _ in users:
        info += f'Имя: {_[1]}, пароль: {_[2]}\n'

    cur.close()  # Закрываем курсор,  close() - функция, которая закрывает соединение с БД
    conn.close()  # Закрываем само соединение,  close() - функция, которая закрывает соединение с БД

    await message.answer(info) # Ответ на вопрос как дела, а не новое сообщение от бота

if __name__ == '__main__':
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')



# strip() - функция, которая удаляет пробелы до и после текста