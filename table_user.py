import sqlite3


def insert_new_user(user, db_name='disney_bot.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    vk_ids = cursor.execute("""SELECT vk_id FROM users""").fetchall()
    if len(vk_ids) > 0:
        for vk_id in vk_ids:
            if vk_id[0] == user[1]:
                return 0
    cursor.execute("""INSERT INTO users (nick, vk_id) VALUES (?, ?)""", user)
    conn.commit()
    return 1


def change_nick(vk_id, new_nick, db_name='disney_bot.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    users = cursor.execute("""SELECT * FROM users""").fetchall()
    for user in users:
        if int(vk_id) == int(user[2]):
            cursor.execute("""UPDATE users 
                SET nick = ?
                WHERE vk_id = ?""", (new_nick, vk_id, ))
            conn.commit()
            return 1
    return 0


def add_experience(vk_id, number_of_points):
    a = 1
    # TODO сделать добавление экспы
