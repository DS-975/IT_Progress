
import logging
import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import router

import calendar
import datetime


# Инициализация бота и диспетчера
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
from aiogram.fsm.storage.memory import MemoryStorage
storage = MemoryStorage()
dp = Dispatcher(storage=storage)







# Месяц
month_name_next = calendar.month_name[int(datetime.datetime.now().strftime("%m"))]

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

