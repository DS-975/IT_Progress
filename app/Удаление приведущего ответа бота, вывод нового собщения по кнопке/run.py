import logging
import asyncio


from aiogram import Bot, Dispatcher

from config import TOKEN





from aiogram import F
from aiogram.types import Message

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

storage = MemoryStorage()




from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery





# Инициализация бота и диспетчера
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
from aiogram.fsm.storage.memory import MemoryStorage
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command ('start'))
async def send_welcome(message: Message):
    await message.answer("Привет! Нажми 'Далее', чтобы получить новый ответ.", reply_markup=main_menu)

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Далее", callback_data="Далее")]
])
# def main_menu():
#     keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(KeyboardButton("Далее"))
#     return keyboard


@dp.callback_query(F.data == "Далее")
async def handle_next(callback_query: CallbackQuery):
    # Удаляем предыдущее сообщение (если оно есть)
    await callback_query.message.delete()  # Удаляем сообщение, на которое нажали кнопку

    # Отправляем новое сообщение с кнопками
    await callback_query.message.answer("Вот новый ответ!", reply_markup=main_menu)

    # Не забудьте ответить на колбэк, чтобы убрать "часики" у кнопки
    await callback_query.answer()

    # Сохраняем ID нового сообщения, если нужно (например, для дальнейшего удаления)
    # можно сохранить в контексте или в каком-то хранилище





# Запуск процесса поллинга новых апдейтов
async def main():
    #dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')