import sqlite3


def get_answer(answer_id):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    try:
        answer = cursor.execute("""
            SELECT title 
            FROM game1_answers 
            WHERE id = ?""", (answer_id,)).fetchall()
        return answer[0]
    except Exception:
        return -1
