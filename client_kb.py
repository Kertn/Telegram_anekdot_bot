from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Анекдот')
b2 = KeyboardButton('/Лучшие_анекдоты')
b3 = KeyboardButton('/Категории_анекдотов')

d1 = KeyboardButton("/Следующий_анекдот")
d2 = KeyboardButton("/Главная")

n1 = KeyboardButton("/Следующий_по_популярности")
n2 = KeyboardButton("/Главная")


kb_anekdot_best = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_anekdot_client = ReplyKeyboardMarkup(resize_keyboard=True)


kb_client.row(b1,b2).add(b3)

kb_anekdot_client.add(d1).row(d2)

kb_anekdot_best.add(n1).add(n2)
