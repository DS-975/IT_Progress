import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from config import TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# "База данных" для хранения заметок (в реальном проекте используйте SQLite/PostgreSQL и т.д.)
notes_db = {}


# Клавиатура с основными командами
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="📝 Добавить заметку"),
        KeyboardButton(text="📋 Мои заметки"),
        KeyboardButton(text="❌ Удалить заметку"),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    notes_db[user_id] = notes_db.get(user_id, [])

    await message.answer(
        "📔 Добро пожаловать в ваш личный блокнот!\n"
        "Вы можете добавлять, просматривать и удалять заметки.",
        reply_markup=get_main_keyboard()
    )


# Обработчик кнопки "Добавить заметку"
@dp.message(F.text == "📝 Добавить заметку")
async def add_note_start(message: types.Message):
    await message.answer("📝 Введите текст заметки:")
    # Устанавливаем состояние (в реальном проекте используйте FSM)


# Обработчик текста заметки
@dp.message(F.text & ~F.text.startswith(('📝', '📋', '❌')))
async def save_note(message: types.Message):
    user_id = message.from_user.id
    note_text = message.text

    if user_id not in notes_db:
        notes_db[user_id] = []

    notes_db[user_id].append(note_text)
    await message.answer(f"✅ Заметка сохранена!\nВсего заметок: {len(notes_db[user_id])}")


# Обработчик кнопки "Мои заметки"
@dp.message(F.text == "📋 Мои заметки")
async def show_notes(message: types.Message):
    user_id = message.from_user.id
    notes = notes_db.get(user_id, [])

    if not notes:
        await message.answer("У вас пока нет заметок.")
        return

    response = "📋 Ваши заметки:\n\n"
    for i, note in enumerate(notes, 1):
        response += f"{i}. {note}\n\n"

    await message.answer(response)


# Обработчик кнопки "Удалить заметку"
@dp.message(F.text == "❌ Удалить заметку")
async def delete_note_start(message: types.Message):
    user_id = message.from_user.id
    notes = notes_db.get(user_id, [])

    if not notes:
        await message.answer("У вас пока нет заметок для удаления.")
        return

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
                     [KeyboardButton(text=f"❌ Удалить {i + 1}")] for i in range(len(notes))
                 ] + [[KeyboardButton(text="🔙 Назад")]],
        resize_keyboard=True
    )

    await message.answer("Выберите заметку для удаления:", reply_markup=keyboard)


# Обработчик удаления конкретной заметки
@dp.message(F.text.startswith("❌ Удалить "))
async def delete_note(message: types.Message):
    user_id = message.from_user.id
    notes = notes_db.get(user_id, [])

    try:
        note_num = int(message.text.split()[2]) - 1
        if 0 <= note_num < len(notes):
            deleted_note = notes.pop(note_num)
            await message.answer(
                f"🗑 Заметка удалена:\n\n{deleted_note}",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer("Неверный номер заметки.", reply_markup=get_main_keyboard())
    except (IndexError, ValueError):
        await message.answer("Пожалуйста, выберите заметку из списка.", reply_markup=get_main_keyboard())


# Обработчик кнопки "Назад"
@dp.message(F.text == "🔙 Назад")
async def back_to_main(message: types.Message):
    await message.answer("Главное меню:", reply_markup=get_main_keyboard())


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())