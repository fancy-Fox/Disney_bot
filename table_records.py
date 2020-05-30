import sqlite3


def change_record(user_id, new_record):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE records 
            SET score = ?
            WHERE user_id = ?""", (new_record, user_id, )).fetchall()
    conn.commit()


def insert_new_record(user_id, new_record):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    records = cursor.execute("""SELECT * FROM records""").fetchall()
    for record in records:
        if record[1] == user_id:
            if int(record[2]) < int(new_record):
                change_record(user_id, new_record)
            return
    cursor.execute("""INSERT INTO records (user_id, score) VALUES (?, ?)""", (user_id, str(new_record), ))
    conn.commit()


def get_all_records():
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    records = cursor.execute("""SELECT * FROM records""").fetchall()
    return records


def get_record_with_user_id(user_id):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    record = cursor.execute("""SELECT score FROM records WHERE user_id = ?""", (user_id, )).fetchall()[0][0]
    return record


# insert_new_record(30806644, 3)


# conn = sqlite3.connect("disney_bot.db")
# cursor = conn.cursor()
# records = cursor.execute("""DELETE FROM records""").fetchall()
# conn.commit()