import sqlite3


def change_record(user_id, new_record, db_name='disney_bot.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("""UPDATE records 
                SET score = ?
                WHERE user_id = ?""", (new_record, user_id, )).fetchall()
        record_id = cursor.execute("""SELECT id 
                        FROM records
                        WHERE user_id = ?""", (user_id, )).fetchall()[0][0]
        cursor.execute("""UPDATE users 
                    SET record_id = ?
                    WHERE vk_id = ?""", (record_id, user_id, ))
        conn.commit()
        return 1
    except Exception:
        return 0


def insert_new_record(user_id, new_record, db_name='disney_bot.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    records = get_all_records(db_name)
    for record in records:
        if record[1] == user_id:
            if int(record[2]) < int(new_record):
                change_record(user_id, new_record)
                return 1
            return 0
    #  TODO check convert to str
    cursor.execute("""INSERT INTO records (user_id, score) VALUES (?, ?)""", (user_id, str(new_record), ))
    conn.commit()
    return 1


def get_all_records(db_name='disney_bot.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    records = cursor.execute("""SELECT * FROM records""").fetchall()
    return records


def get_record_with_user_id(user_id, db_name='disney_bot.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        record = cursor.execute("""SELECT score FROM records WHERE user_id = ?""", (user_id, )).fetchall()[0][0]
        return record
    except Exception:
        return -1
