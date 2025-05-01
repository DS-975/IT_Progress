from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

storage = MemoryStorage()

import calendar
import datetime


import keyboards as kb
from run_calendar import month_name_next



router_ = "some_value"  # Пример определения объекта router
# router = Router()

# handlers
# Хэндлер на команду /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name} !\n'
                          f'\n'
                          f'Функции теста Календаря :',
                          reply_markup = await kb.current_calendar())


# async def catalog(callback: CallbackQuery):
#     await callback.answer('Вы выбрали следующий месяц',
@router.callback_query(F.data == f'>_{month_name_next}')
async def next_m(callback_query: CallbackQuery):

    # Удаляем предыдущее сообщение (если оно есть)
    await callback_query.message.delete()  # Удаляем сообщение, на которое нажали кнопку

    # Отправляем новое сообщение с кнопками
    await callback_query.message.answer('Вы выбрали следующий месяц',
                         reply_markup = await kb.next_calendar(month_name_next)) # Выскакивает комментарий в центре и сразу пропадает

    # Не забудьте ответить на колбэк, чтобы убрать "часики" у кнопки
    await callback_query.answer()






@router.callback_query(F.data == 'contacts')
async def contacts(callback: CallbackQuery):
    await callback.answer('Вы выбрали Контакты', show_alert=True) # Выскакивает комментарий в центре и ждёт когда нажмёте на OK
    await callback.message.answer(f'Привет, вы нажали на - Контакты !') # Сообщение от бота под онлайн кнопками

    #await callback.message.answer(f'Привет, вы нажали на - Каталог !') # Сообщение от бота под онлайн кнопками


@router.message(Command("dice"))
async def cmd_dice(message: Message):
    await message.answer_dice(emoji="🎲")


# Тест Хэндлеров

# Хэндлер на команду /help
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Список команд для этого бота\n'
                         '\n'
                         '/calendar - вывести календарь\n'
                         '/dice - бросить кубик\n'
                         '/help - просмотр команд\n'
                         '/start - запуск бота\n')




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

