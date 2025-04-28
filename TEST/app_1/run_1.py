
import logging
import asyncio

from aiogram import Bot, Dispatcher

from config.config import TOKEN
from app_0.handlers import router



# Инициализация бота и диспетчера
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
from aiogram.fsm.storage.memory import MemoryStorage
storage = MemoryStorage()
dp = Dispatcher(storage=storage)




# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')



#
#
# # Включаем логирование
# logging.basicConfig(level=logging.INFO)

# # Проверка наличия токена
# if TOKEN is None:
#     raise ValueError("TOKEN is not set! Please check your configuration.")




# Импортируются необходимые модули из aiogram.
# BOT_TOKEN — ваш токен доступа. Обязательно замените YOUR_TELEGRAM_BOT_TOKEN на свой токен.
# Настраивается логирование для отладки.
# Создаются объекты Bot и Dispatcher.
# @dp.message(CommandStart()) — декоратор, который регистрирует функцию command_start_handler как обработчик команды /start.
# @dp.message() — декоратор, который регистрирует функцию echo_handler как обработчик всех текстовых сообщений.
# async def — ключевое слово, обозначающее асинхронные функции.
# await — ключевое слово, которое используется для ожидания выполнения асинхронной операции.
# message.answer() — отправляет ответное сообщение пользователю.
# message.send_copy() - отправляет копию сообщения пользователя.
# asyncio.run(main()) — запускает асинхронный цикл событий.
