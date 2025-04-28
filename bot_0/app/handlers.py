from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

storage = MemoryStorage()


# from aiogram import Bot
# from config import TOKEN
# bot = Bot(token=TOKEN)


import calendar
import datetime


import app.keyboards as kb



router = Router()

# handlers
# Хэндлер на команду /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await  message.answer(f'Привет, {message.from_user.first_name} !\n'
                          f'\n'
                          f'Что я умею делать :\n'
                          f'\n'
                          f'- График обучения\n'
                          '     - Кто, когда может присутствовать на обучение \n'
                          '       (Бот будет за этим следить и \n'
                          '        напоминать за 20 минут до урока в этот день\n'
                          '        Писать о прогулах и фиксить это в статистику)\n'
                          '     \n'
                          '     - Вывод статистики по обучению\n'
                          '       - ИМЯ\n'
                          '       - Был на обучение в такой-то день\n'
                          '       - Учился столько-то часов\n'
                          '       - Изучил вот это\n' 
                          '       - Выходил в звонок \n'
                          '     \n'
                          '     - Выводить информацию по встречам (Звонок)\n'
                          '       - Когда были встречи\n'
                          '       - Кто присутствовал на встрече \n'
                          '     \n'
                          '     - Вывод информации, кто когда приступил к обучению\n'
                          '       (Например, \n'
                          '               - ИМЯ готов учиться сейчас, \n'
                          '               - Отошёл ИМЯ (отходить можно !> 10 минут),\n'
                          '                        если не отписался просто\n'
                          '                        остальное время не идёт в отчёт\n'
                          '               - ИМЯ на сегодня закончил учёбу\n'
                          '     \n' 
                          '     - Фиксить прогресс через БД \n'
                          '       и выводить в определенное время статистику \n'
                          '       по ученикам (Кто присутствует, \n'
                          '                    какое направление, \n'
                          '                    соответствие с графиком обучения,\n'
                          '                    были созвоны, \n'
                          '                    включал демку)\n',
                          reply_markup=await kb.inline_cars())


# Хэндлер на команду /help
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Список команд для этого бота\n'
                         '\n'
                         '/calendar - вывести календарь\n'
                         '/dice - бросить кубик\n'
                         '/help - просмотр команд\n'
                         '/start - запуск бота\n')

# меджек фильтр - F
@router.message(F.text == 'Как дела?')
async def how_are_you(message: Message):
    await message.reply('Хорошо!') # Ответ на вопрос как дела, а не новое сообщение от бота

@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')

@router.message(Command('get_photo'))
async def get_photo_1(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAM1aAefQYvH00wxUPUCTssxH0R1pCUAAt4UMhuXyTlIu9tWJ3AV-P4BAAMCAAN5AAM2BA',
                               caption='Это твоё фото ?')



@router.message(Command('main_2'))
async def main_2(message: Message):
    await  message.answer(f'Привет, {message.from_user.first_name} !',
                          reply_markup=kb.main_2)


@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('Вы выбрали каталог') # Выскакивает комментарий в центре и сразу пропадает
    await callback.message.answer(f'Привет, вы нажали на - Каталог !') # Сообщение от бота под онлайн кнопками


@router.callback_query(F.data == 'contacts')
async def contacts(callback: CallbackQuery):
    await callback.answer('Вы выбрали Контакты', show_alert=True) # Выскакивает комментарий в центре и ждёт когда нажмёте на OK
    await callback.message.answer(f'Привет, вы нажали на - Контакты !') # Сообщение от бота под онлайн кнопками


# Тест Хэндлеров

@router.message(Command("dice"))
async def cmd_dice(message: Message):
    await message.answer_dice(emoji="🎲")




# @router.my_chat_member()
# async def on_bot_added(event: ChatMemberUpdated):
#     if event.new_chat_member.status == "member":
#         chat = event.chat
#         await bot.send_message(chat.id, "Спасибо за приглашение!\n\nЯ готов работать.")
#



# # Хэндлер для всех сообщений в группах
# @router.message(F.chat.type.in_({"group", "supergroup"}))
# async def handle_group_message(message: Message):
#     # Пример: отвечаем на любое сообщение в группе
#     await message.reply(f"Вы написали: {message.text}")




















@router.message(Command('calendar'))
async def send_calendar(message:Message):
    await message.answer(text=f'Календарь на {calendar.month_name[int(datetime.datetime.now().strftime("%m"))]}  Выберите дату:',
                         reply_markup = await kb.inline_calendar())


@router.callback_query(F.data == '1')
async def catalog(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали - 1')


# _____________________________________________________
# Работа с

