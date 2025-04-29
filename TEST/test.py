
import logging
import asyncio
import sqlite3

from bot_0.config import TOKEN
from bot_0.app.handlers import router

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup






# Инициализация бота и диспетчера
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
storage = MemoryStorage()
dp = Dispatcher(storage=storage)




# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

# Определяем состояния
class Form(StatesGroup):
    waiting_for_username = State()

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
    await message.answer( 'Привет, сейчас тебя зарегистрируем!\n''Введите ваше имя')

    # Устанавливаем состояние ожидания имени пользователя через вспомогательную функцию
    await set_user_state(state, Form.waiting_for_username)



@dp.message(Form.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    user_name = message.text  # Получаем имя пользователя из сообщения

    await message.answer(f"Ваше имя пользователя: {user_name}")

    await state.clear()  # Завершаем состояние



if __name__ == '__main__':
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')



# strip() - функция, которая удаляет пробелы до и после текста