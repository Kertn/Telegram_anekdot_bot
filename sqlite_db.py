import sqlite3 as sq
from telegram_anekdotov_bot.create_bot import bot
from telegram_anekdotov_bot.keyboards import client_inline



base = sq.connect('anekdot.db')
cur = base.cursor()
if base:
    print('Data base successfully connected')
base.execute('CREATE TABLE IF NOT EXISTS data(anekdot TEXT PRIMARY KEY, number, likes, dislikes)')
base.commit()

base_anek = sq.connect('anekdot_id.db')
cur_anek = base_anek.cursor()
if base_anek:
    print('Data base user_id successfully connected')
base_anek.execute('CREATE TABLE IF NOT EXISTS data_id(id TEXT PRIMARY KEY, list)')
base_anek.commit()

async def sql_id(user_id):
    cur_anek.execute('INSERT INTO data_id VALUES (?, ?)', (user_id, 0))
    base_anek.commit()


async def sql_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO data VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read(message, user_id):
    try:
        with open("C:\Program\Projects\TelegramProjects\\telegram_anekdotov_bot\count.txt", "r") as file:
            read = file.read()

        def random():
            import random
            random_number = random.randint(1, int(read)-1)

            ff = str(random_number)
            anekdot_li(ff)

        watched = cur_anek.execute('SELECT list FROM data_id WHERE id == ?', (user_id,)).fetchall()

        try:
            watched_list = watched[0][0].split(" ")
        except:
            watched_list = [watched[0][0]]

        print(watched)
        final = len(watched_list)

        def anekdot_li(ff):
            count_final = 0
            for anek in watched_list:
                print(anek)
                print(ff)
                if anek == ff:
                    print("nie")
                    random()
                else:
                    print("tak")
                    count_final += 1
                    if count_final == final:
                        global da
                        da = ff
                        print(da)
        random()


        for ret in cur.execute('SELECT * FROM data WHERE number == ?', (da,)).fetchall():
            await bot.send_message(message.from_user.id, f'{ret[0]}\n', reply_markup=client_inline.inkb)
            global numer_anekdot
            numer_anekdot = str(ret[1])
            with open("anekdot.txt", "w") as file:
                file.write(numer_anekdot)
                file.close()

        values = cur_anek.execute('SELECT list FROM data_id WHERE id == ?', (user_id,)).fetchall()
        values_new = str(values[0][0]) + f" {numer_anekdot}"
        print(values_new)
        cur_anek.execute('UPDATE data_id SET list == ? WHERE id == ?', (values_new, user_id))
        base_anek.commit()
        print("11")
    except:
        await bot.send_message(message.from_user.id, 'Анекдоты закончились  😞. Приходите позже!')

async def best_sql_read(message, user_id):

    all_likes = cur.execute('SELECT likes FROM data').fetchall()

    watched = cur_anek.execute('SELECT list FROM data_id WHERE id == ?', (user_id,)).fetchall()


    print(watched)
    try:
        watched_list = watched[0][0].split(" ")
    except:
        watched_list = [watched[0][0]]

    print(all_likes)
    print(sorted(all_likes))

    sorted_likes = sorted(all_likes)

    print(watched_list)

    print(sorted_likes)

    try:
        anek_count = 1
        def best_anek(anek_count):
            like = sorted_likes[-anek_count][0]
            global numer_anek
            numer_anek = cur.execute('SELECT number FROM data WHERE likes == ?', (like,)).fetchall()
            print(numer_anek, " Nowy")
            anekdot_li(numer_anek, anek_count)

        final = len(watched_list)
        print(final)
        def anekdot_li(numer_anek, anek_count):
            count_final = 0
            for anek in watched_list:
                print(anek)
                print(numer_anek[0][0])
                if anek == numer_anek[0][0]:
                    print("nie")
                    anek_count += 1
                    print(anek_count)
                    best_anek(anek_count)
                else:
                    print("tak")
                    count_final += 1
                    if count_final == final:
                        global best
                        best = numer_anek[0][0]
                        print(best)
        best_anek(anek_count)
        print(best)

        for ret in cur.execute('SELECT * FROM data WHERE number == ?', (best,)).fetchall():
            await bot.send_message(message.from_user.id, f'{ret[0]}\n', reply_markup=client_inline.inkb)
            global numer_anekdot
            numer_anekdot = str(ret[1])
            with open("anekdot.txt", "w") as file:
                file.write(numer_anekdot)
                file.close()

        values = cur_anek.execute('SELECT list FROM data_id WHERE id == ?', (user_id,)).fetchall()
        values_new = str(values[0][0]) + f" {numer_anekdot}"
        print(values_new)
        cur_anek.execute('UPDATE data_id SET list == ? WHERE id == ?', (values_new, user_id))
        base_anek.commit()
        print("11")
    except:
        await bot.send_message(message.from_user.id, 'Анекдоты закончились  😞. Приходите позже!')


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
        dislike = int(dislike[0][0]) + int(res)
        cur.execute('UPDATE data SET dislikes = ? WHERE number == ?', (dislike, numer_anekdot))
        base.commit()

    else:
        global like
        like = cur.execute('SELECT likes FROM data WHERE number == ?', (numer_anekdot,)).fetchall()
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

    return like, dislike