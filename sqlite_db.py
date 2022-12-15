import sqlite3 as sq
from telegram_anekdotov_bot.create_bot import bot
from telegram_anekdotov_bot.keyboards import client_inline
import random

numer_anekdot_list = [" "]

global base, cur
base = sq.connect('anekdot.db')
cur = base.cursor()
if base:
    print('Data base successfully connected')
base.execute('CREATE TABLE IF NOT EXISTS data(anekdot TEXT PRIMARY KEY, number, likes, dislikes)')
base.commit()

async def sql_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO data VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    with open("C:\Program\Projects\TelegramProjects\\telegram_anekdotov_bot\count.txt", "r") as file:
        read = file.read()

    random_number = random.randint(1, int(read)-1)

    ff = str(random_number)

    for ret in cur.execute('SELECT * FROM data WHERE number == ?', (ff,)).fetchall():
        await bot.send_message(message.from_user.id, f'{ret[0]}\n', reply_markup=client_inline.inkb)
        global numer_anekdot
        numer_anekdot = str(ret[1])
        print(numer_anekdot_list)
        with open("anekdot.txt", "w") as file:
            file.write(numer_anekdot)
            file.close()



async def sql_read2():
    return cur.execute('SELECT * FROM data').fetchall()

async def sql_delete_command(data):
    cur.execute('DELETE FROM data WHERE number == ?', (data,))
    base.commit()

async def sql_like_count(res):
    if int(res) < 0:
        global like
        global dislike
        dislike = cur.execute('SELECT dislikes FROM data WHERE number == ?', (numer_anekdot,)).fetchall()
        print(numer_anekdot)
        print(dislike[0][0])
        dislike = int(dislike[0][0]) + int(res)
        cur.execute('UPDATE data SET dislikes = ? WHERE number == ?', (dislike, numer_anekdot))
        base.commit()

    else:
        global like
        like = cur.execute('SELECT likes FROM data WHERE number == ?', (numer_anekdot,)).fetchall()
        print(numer_anekdot)
        print(like[0][0])
        like = int(like[0][0]) + int(res)
        cur.execute('UPDATE data SET likes = ? WHERE number == ?', (like, numer_anekdot))
        base.commit()

def pomogite():
    with open("anekdot.txt", "r") as file:
        numer_anekdot = file.read()


    print(numer_anekdot)
    like_2 = cur.execute('SELECT likes FROM data WHERE number == ?', (numer_anekdot,)).fetchall()
    dislike_2 = cur.execute('SELECT dislikes FROM data WHERE number == ?', (numer_anekdot,)).fetchall()

    like = like_2[0][0]
    dislike = dislike_2[0][0]
    print("pomogite")

    return like, dislike