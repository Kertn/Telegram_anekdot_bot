from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token="5587534898:AAHU-toKADiVSNYIeu84JRGiggKw36hwD9s")
dp = Dispatcher(bot, storage=storage)