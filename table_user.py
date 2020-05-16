import sqlite3


def insert_new_user(user):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    vk_ids = cursor.execute("""SELECT vk_id FROM users""").fetchall()
    for vk_id in vk_ids[0]:
        if vk_id == user[1]:
            return 0
    cursor.execute("""INSERT INTO users (name, vk_id, role) VALUES (?, ?)""", user)
    conn.commit()
    return 1
