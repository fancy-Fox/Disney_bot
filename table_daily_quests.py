import sqlite3
import time


def get_all_daily_quest_info():
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    try:
        return cursor.execute("""SELECT * FROM daily_quests""").fetchall()[0]
    except Exception:
        return []


def insert_new_daily_quest(new_quest):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO daily_quests (type, date, user_id) VALUES (?, ?, ?) """, new_quest)
        conn.commit()
        return 1
    except Exception:
        return 0


def drop_all_daily_quests_info():
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""DELETE FROM daily_quests""")
        conn.commit()
        return 1
    except Exception:
        return 0


def try_to_delete_daily_quest(daily_quest):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""DELETE FROM daily_quests WHERE type = ? and user_id = ? """, daily_quest)
        conn.commit()
        return 1
    except Exception:
        return 0


def try_to_insert_new_daily_quest(new_quest):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    try:
        quest_time = cursor.execute("""SELECT date 
                                        FROM daily_quests 
                                        WHERE user_id = ? and type = ?""", (new_quest[2], new_quest[0])).fetchall()[0][0]
    except Exception:
        quest_time = time.time()
    if time.time() - quest_time >= 86400:
        cursor.execute("""UPDATE daily_quests 
            SET date = ?
            WHERE user_id = ? and type = ?""", (new_quest[1], new_quest[2], new_quest[0], ))
        conn.commit()
        return 1
    else:
        return 0
