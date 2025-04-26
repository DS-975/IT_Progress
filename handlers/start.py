# handlers/.py
from aiogram import types, Dispatcher
from aiogram.filters import Command

# Обработчик команды /start
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот. Как я могу помочь?")

# Функция для регистрации обработчиков
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, Command("start"))
