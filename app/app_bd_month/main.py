
import logging
import asyncio

from aiogram import Bot, Dispatcher

from app.app_bd_month.c_h_k.config import TOKEN
from app.app_bd_month.c_h_k.handlers import router, drop_table_months


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
        # Удалить БД
        drop_table_months()
        print('Exit')

