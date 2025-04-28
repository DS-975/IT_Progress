import calendar
import datetime
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Замените 'YOUR_API_TOKEN' на ваш токен бота
from bot_0.config import TOKEN
API_TOKEN = TOKEN

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def create_calendar(year, month):
    keyboard = []

    # Добавляем кнопки для навигации по месяцам
    if month > 1:
        keyboard.append([InlineKeyboardButton("Назад", callback_data=f"navigate:{year}:{month - 1}")])
    if month < 12:
        keyboard.append([InlineKeyboardButton("Вперед", callback_data=f"navigate:{year}:{month + 1}")])

    # Добавляем дни месяца
    days_buttons = []
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        days_buttons.append(InlineKeyboardButton(text=str(day), callback_data=f"day:{year}:{month}:{day}"))

        # Если добавлено 7 кнопок (неделя), добавляем их в клавиатуру и начинаем новую строку.
        if len(days_buttons) == 7:
            keyboard.append(days_buttons)
            days_buttons = []

    # Добавляем оставшиеся дни (если есть)
    if days_buttons:
        keyboard.append(days_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message(Command('start'))
async def start_command(message: types.Message):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    calendar_markup = await create_calendar(current_year, current_month)

    await message.answer("Выберите дату:", reply_markup=calendar_markup)


@dp.callback_query(lambda c: c.data.startswith("day:"))
async def day_selected(callback_query: types.CallbackQuery):
    _, year, month, day = callback_query.data.split(":")

    await callback_query.message.answer(f"Вы выбрали {day} {calendar.month_name[int(month)]} {year}.")


@dp.callback_query(lambda c: c.data.startswith("navigate:"))
async def navigate_month(callback_query: types.CallbackQuery):
    _, year, month = callback_query.data.split(":")

    calendar_markup = await create_calendar(int(year), int(month))

    await callback_query.message.edit_reply_markup(reply_markup=calendar_markup)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')