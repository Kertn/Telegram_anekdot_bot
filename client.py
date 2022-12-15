from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardRemove
from keyboards.client_kb import kb_client, kb_anekdot_client
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import client_inline


async def start(message:types.Message):
    await bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=kb_client)

async def anekdot(message: types.Message):
    await bot.send_message(message.from_user.id, 'Веселого настроения!', reply_markup=kb_anekdot_client)
    await sqlite_db.sql_read(message)

async def anekdot_next(message: types.Message):
    await sqlite_db.sql_read(message)


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
    dp.register_message_handler(anekdot_next, commands=['Следующий_анекдот'])

