import client, admin #other
from aiogram.utils import executor
from create_bot import bot, dp
from data_base import sqlite_db

async def on_startup(_):
	print('Бот вышел в онлайн')


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)