from aiogram import Dispatcher
from aiogram import Bot, types
from aiogram.utils import executor
import asyncio
import os
from telegram_anekdotov_bot.data_base import sqlite_db
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

answ = dict()

# inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Нажми меня', callback_data='www'))
#
# @dp.message_handler(commands='test')
# async def test_commands(message:types.Message):
#     await message.answer("Инлайн кнопка", reply_markup=inkb)
#
# @dp.callback_query_handler(text='www')
# async def www_call(callback : types.CallbackQuery):
#     await callback.answer('Нажата инлайн кнопка', show_alert=True)

inkb = InlineKeyboardMarkup(row_width=1)#.add(InlineKeyboardButton(text='        Нравится        👍', callback_data='like_1'),\
                                             #InlineKeyboardButton(text='Не нравится    👎', callback_data='like_-1'))

b1 = InlineKeyboardButton(text='Нравится      👍', callback_data='like_1')
b2 = InlineKeyboardButton(text='Не нравится     👎', callback_data='like_-1')

inkb.row(b1, b2)

#inkb_likes = InlineKeyboardMarkup(row_width=1)

def likes():
    inkb_likes = InlineKeyboardMarkup(row_width=1)

    print('121212')

    like, dislike = sqlite_db.pomogite()

    d1 = InlineKeyboardButton(text=f'{like}      👍', callback_data='like_1')
    d2 = InlineKeyboardButton(text=f'{dislike}    👎', callback_data='like_-1')

    inkb_likes.row(d1, d2)

    return inkb_likes



# async def www_call(callback : types.CallbackQuery):
#     res = int(callback.data.split('_')[1])
#     if callback.from_user.id not in answ:
#         await callback.answer('Вы проголосовали')
#         answ[callback.from_user.id] = res
#     else:
#         await callback.answer('Вы уже проголосовали', show_alert=True)


