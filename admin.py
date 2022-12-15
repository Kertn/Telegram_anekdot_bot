from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = ""
ID_admin = "5703686837"


class FSMAdmin(StatesGroup):
    anekdot = State()
    number = State()
    likes = State()
    dislikes = State()

async def admin_start(message: types.Message):
    global ID
    ID = message.from_user.id
    if str(ID) == ID_admin:
        await bot.send_message(message.from_user.id, 'Чего желаете, мой повелитель?', reply_markup=admin_kb.button_case_admin)
    else:
        await bot.send_message(message.from_user.id, 'Нету доступа!')

async def cancel_hendler(message: types.Message, state: FSMContext):
    if str(ID) == ID_admin:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("Done")

async def add_anekdot(message:types.Message):
    if str(ID) == ID_admin:
        await FSMAdmin.anekdot.set()
        await bot.send_message(message.from_user.id, "Анекдот: ")
    else:
        await bot.send_message(message.from_user.id, 'Нету доступа!')


# async def load_name(message: types.Message, state: FSMContext):
#     if str(message.from_user.id) == ID_admin:
#         async with state.proxy() as data:
#             data["name"] = message.text
#         await FSMAdmin.next()
#         await message.reply("Введите сам анекдот: ")
#     else:
#         await bot.send_message(message.from_user.id, 'Нету доступа!')

async def load_disc(message: types.Message, state: FSMContext):
    with open('count.txt', "r") as file:
        count = file.read()


    if str(message.from_user.id) == ID_admin:
        async with state.proxy() as data:
            data["anekdot"] = message.text
            data["number"] = count
            data["likes"] = "0"
            data["dislikes"] = "0"

        await message.reply("Готово", reply_markup=admin_kb.button_case_admin)

        await sqlite_db.sql_command(state)

        t = int(count) + 1

        with open('count.txt', 'w') as file:
            file.write(str(t))

        await state.finish()
    else:
       await bot.send_message(message.from_user.id, 'Нету доступа!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)

    with open('count.txt', "r") as file:
        count = file.read()

    t = int(count) - 1

    with open('count.txt', 'w') as file:
        file.write(str(t))

async def delete_item(message: types.Message):
    if str(ID) == ID_admin:
       read = await sqlite_db.sql_read2()
       for ret in read:
            await bot.send_message(message.from_user.id, ret[0])
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Удалить', callback_data=f'del {ret[1]}')))



def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(admin_start, commands=['admin'])
    dp.register_message_handler(add_anekdot, commands=['Загрузить'])
    dp.register_message_handler(cancel_hendler, state="*", commands='/отмена')
    dp.register_message_handler(cancel_hendler, Text(equals='отмена', ignore_case=True), state="*")
    #dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_disc, state=FSMAdmin.anekdot)
    dp.register_message_handler(delete_item, commands=['Удалить'])