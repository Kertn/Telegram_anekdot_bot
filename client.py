from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardRemove
from keyboards.client_kb import kb_client, kb_anekdot_client, kb_anekdot_best
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import client_inline

user_id = ""

async def start(message:types.Message):
    await bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=kb_client)
    global user_id
    user_id = message.from_user.id
    await sqlite_db.sql_id(user_id)

async def anekdot(message: types.Message):
    await bot.send_message(message.from_user.id, 'Веселого настроения!', reply_markup=kb_anekdot_client)
    await sqlite_db.sql_read(message, message.from_user.id)

async def kategor(message: types.Message):
    await bot.send_message(message.from_user.id, 'Эта функция еще не готова!')


async def anekdot_next(message: types.Message):
    await sqlite_db.sql_read(message, message.from_user.id)

async def best_anekdot(message: types.Message):
    await bot.send_message(message.from_user.id, 'Лучшие анекдоты' , reply_markup=kb_anekdot_best)
    await sqlite_db.best_sql_read(message, message.from_user.id)

async def best_anekdot_next(message: types.Message):
    await sqlite_db.best_sql_read(message, message.from_user.id)


async def anekdot_past(message: types.Message):
    await bot.send_message(message.from_user.id, 'Главная страница', reply_markup=kb_client)


@dp.callback_query_handler(Text(startswith='like_'))
async def www_call(callback : types.CallbackQuery):
    answ = dict()
    res = int(callback.data.split('_')[1])
    if callback.from_user.id not in answ:
        await sqlite_db.sql_like_count(res)
        #await callback.answer('Вы проголосовали')
        #client_inline.likes()
        await bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=client_inline.likes()
        )

    else:
        await callback.answer('Вы уже проголосовали', show_alert=True)

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(anekdot, commands=['Анекдот'])
    dp.register_message_handler(best_anekdot, commands=['Лучшие_анекдоты'])
    dp.register_message_handler(best_anekdot_next, commands=['Следующий_по_популярности'])
    dp.register_message_handler(anekdot_next, commands=['Следующий_анекдот'])
    dp.register_message_handler(anekdot_past, commands=['Главная'])
    dp.register_message_handler(kategor, commands=['Категории_анекдотов'])

