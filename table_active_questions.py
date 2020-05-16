import sqlite3


def is_user_in_game(user_id):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    try:
        count_of_questions = cursor.execute("""
        SELECT count(*) 
        FROM active_questions 
        WHERE user_id = ?""", (user_id,)).fetchall()
        return count_of_questions[0][0] > 0
    except Exception:
        return False


def get_active_question(user_id):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    try:
        last_question = cursor.execute("""
            SELECT question_id 
            FROM active_questions 
            WHERE user_id = ? AND last_question == True""", (user_id,)).fetchall()[0]
        return last_question
    except Exception:
        return -1


def remove_all_question_for_user(user_id):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM active_questions  
        WHERE user_id = ?""", (user_id,)).fetchall()
    conn.commit()


def add_new_question(user_id, question_id):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""UPDATE active_questions 
            SET last_question = False
            WHERE user_id = ? AND last_question = True""", (user_id,))
        conn.commit()
    except Exception:
        a = 1        # TODO сделать тут что-то
    cursor.execute("""INSERT INTO active_questions (user_id, question_id, last_question) 
            VALUES (?, ?, ?) 
            """, (int(user_id), int(question_id), True, ))
    conn.commit()


add_new_question(30806644, 1)