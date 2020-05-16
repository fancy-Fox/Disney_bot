import sqlite3

import table_active_questions


def get_question(question_id):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    try:
        question = cursor.execute("""
            SELECT * 
            FROM game1_questions 
            WHERE id = ?""", (question_id,)).fetchall()
        return question
    except Exception:
        return -1


def get_some_question(user_id):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    count_of_questions = cursor.execute("""
                SELECT count(*) 
                FROM game1_questions""").fetchall()
    used_questions = cursor.execute("""
                SELECT question_id 
                FROM active_questions 
                WHERE user_id = ?""", (user_id,)).fetchall()
    list_of_used_questions = []
    for question in used_questions:
        list_of_used_questions.append(question[0])
    if len(list_of_used_questions) == count_of_questions:
        return {"victory"}
    question_ids = cursor.execute("""
                    SELECT id 
                    FROM game1_questions""").fetchall()
    for question_id in question_ids:
        if question_id[0] not in list_of_used_questions:
            table_active_questions
            return question_id
    return {'error'}


def get_correct_answer(question_id):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    try:
        correct_answer = cursor.execute("""
                        SELECT correct_answer_id
                        FROM game1_questions
                        WHERE id = ?
                        """, (question_id,)).fetchall()
        return correct_answer[0]
    except Exception:
        return -1


def get_number_of_answer_with_question_id_and_position(question_id, position):
    conn = sqlite3.connect("disney_bot.db")
    cursor = conn.cursor()
    try:
        question = cursor.execute("""
                            SELECT *
                            FROM game1_questions
                            WHERE id = ?
                            """, (question_id,)).fetchall()
        if position == 1:
            return question[0][2]
        elif position == 2:
            return question[0][3]
        elif position == 3:
            return question[0][4]
        elif position == 4:
            return question[0][5]
        else:
            return -1
    except Exception:
        return -1

# print(get_number_of_answer_with_question_id_and_position(1, 1))
