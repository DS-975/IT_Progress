import logging
import asyncpg
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
import os

# Загрузка конфигурации
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Состояния FSM
class NoteStates(StatesGroup):
    waiting_for_note_text = State()
    waiting_for_note_delete = State()


# Класс для работы с PostgreSQL
class Database:
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            min_size=1,  # Минимальное количество соединений
            max_size=10,  # Максимальное количество
            command_timeout=60,  # Таймаут запросов (сек)
            timeout=10  # Таймаут подключения
        )
        await self._create_tables()

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            try:
                return await conn.execute(query, *args)
            except asyncpg.exceptions.ConnectionDoesNotExistError:
                await self.connect()  # Переподключение
                return await conn.execute(query, *args)

    async def _create_tables(self):
        async with self.pool.acquire() as conn:
            try:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id BIGINT PRIMARY KEY,
                        username TEXT
                    )
                """)
            except asyncpg.exceptions.ConnectionDoesNotExistError:
                # Переподключение при ошибке
                await asyncio.sleep(1)
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS notes (
                        note_id SERIAL PRIMARY KEY,
                        user_id BIGINT REFERENCES users(user_id),
                        text TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                """)

    async def add_user(self, user_id: int, username: str):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO users (user_id, username)
                VALUES ($1, $2)
                ON CONFLICT (user_id) DO NOTHING
            """, user_id, username)

    async def add_note(self, user_id: int, text: str):
        async with self.pool.acquire() as conn:
            return await conn.fetchval("""
                INSERT INTO notes (user_id, text)
                VALUES ($1, $2)
                RETURNING note_id
            """, user_id, text)

    async def get_notes(self, user_id: int):
        async with self.pool.acquire() as conn:
            return await conn.fetch("""
                SELECT note_id, text 
                FROM notes 
                WHERE user_id = $1
                ORDER BY created_at DESC
            """, user_id)

    async def delete_note(self, user_id: int, note_id: int):
        async with self.pool.acquire() as conn:
            return await conn.execute("""
                DELETE FROM notes
                WHERE user_id = $1 AND note_id = $2
            """, user_id, note_id)


# Инициализация базы данных
db = Database()


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
    username = message.from_user.username or "unknown"

    await db.add_user(user_id, username)
    await message.answer(
        "📔 Добро пожаловать в ваш личный блокнот!\n"
        "Вы можете добавлять, просматривать и удалять заметки.",
        reply_markup=get_main_keyboard()
    )


# Обработчик кнопки "Добавить заметку"
@dp.message(F.text == "📝 Добавить заметку")
async def add_note_start(message: types.Message, state: FSMContext):
    await message.answer("📝 Введите текст заметки:")
    await state.set_state(NoteStates.waiting_for_note_text)


# Обработчик текста заметки (в состоянии ожидания текста)
@dp.message(NoteStates.waiting_for_note_text)
async def save_note(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    note_text = message.text

    note_id = await db.add_note(user_id, note_text)
    notes = await db.get_notes(user_id)

    await message.answer(f"✅ Заметка #{note_id} сохранена!\nВсего заметок: {len(notes)}")
    await state.clear()


# Обработчик кнопки "Мои заметки"
@dp.message(F.text == "📋 Мои заметки")
async def show_notes(message: types.Message):
    user_id = message.from_user.id
    notes = await db.get_notes(user_id)

    if not notes:
        await message.answer("У вас пока нет заметок.")
        return

    response = "📋 Ваши заметки:\n\n"
    for note in notes:
        response += f"#{note['note_id']}: {note['text']}\n\n"

    await message.answer(response)


# Обработчик кнопки "Удалить заметку"
@dp.message(F.text == "❌ Удалить заметку")
async def delete_note_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    notes = await db.get_notes(user_id)

    if not notes:
        await message.answer("У вас пока нет заметок для удаления.")
        return

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
                     [KeyboardButton(text=f"❌ Удалить #{note['note_id']}")] for note in notes
                 ] + [[KeyboardButton(text="🔙 Назад")]],
        resize_keyboard=True
    )

    await message.answer("Выберите заметку для удаления:", reply_markup=keyboard)
    await state.set_state(NoteStates.waiting_for_note_delete)


# Обработчик удаления конкретной заметки
@dp.message(NoteStates.waiting_for_note_delete, F.text.startswith("❌ Удалить #"))
async def delete_note(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        note_id = int(message.text.split("#")[1])
        deleted = await db.delete_note(user_id, note_id)

        if deleted == "DELETE 1":
            await message.answer(
                f"🗑 Заметка #{note_id} удалена!",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer(
                "Заметка не найдена или уже удалена.",
                reply_markup=get_main_keyboard()
            )
    except (IndexError, ValueError):
        await message.answer(
            "Пожалуйста, выберите заметку из списка.",
            reply_markup=get_main_keyboard()
        )

    await state.clear()


# Обработчик кнопки "Назад" (выход из состояний)
@dp.message(F.text == "🔙 Назад")
async def back_to_main(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню:", reply_markup=get_main_keyboard())


# Запуск бота
async def main():
    await db.create_pool()
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')