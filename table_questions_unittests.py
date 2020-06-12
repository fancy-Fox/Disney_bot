import sqlite3
import unittest

import table_questions

test_db_name = 'disney_bot_test.db'
true_db_name = 'disney_bot.db'


def remove_everything_from_test_user_db():
    conn = sqlite3.connect(test_db_name)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM game1_questions""")
    conn.commit()


def fill_table():
    true_conn = sqlite3.connect(true_db_name)
    true_cursor = true_conn.cursor()
    values = true_cursor.execute("""SELECT * FROM game1_questions""").fetchall()
    test_conn = sqlite3.connect(test_db_name)
    test_cursor = test_conn.cursor()
    for value in values:
        test_cursor.execute("""INSERT INTO game1_questions VALUES (?, ?, ?, ?, ?, ?, ?)""", value)
    test_conn.commit()


class TestTableQuestions(unittest.TestCase):

    def test_getting_question(self):
        remove_everything_from_test_user_db()
        fill_table()
        some_question = table_questions.get_question(1, test_db_name)
        correct_id = 1
        first_answer = 6
        second_answer = 2
        third_answer = 3
        fourth_answer = 4
        correct_answer = 6
        self.assertEqual(some_question[0], correct_id)  # id
        # checking answers_id
        self.assertEqual(some_question[2], first_answer)
        self.assertEqual(some_question[3], second_answer)
        self.assertEqual(some_question[4], third_answer)
        self.assertEqual(some_question[5], fourth_answer)
        self.assertEqual(some_question[6], correct_answer)
        self.assertEqual(table_questions.get_question(-1, test_db_name), -1)
        self.assertEqual(table_questions.get_question(99999, test_db_name), -1)
        remove_everything_from_test_user_db()

    def test_getting_correct_answer(self):
        remove_everything_from_test_user_db()
        fill_table()
        correct_answer = table_questions.get_correct_answer(1, test_db_name)
        self.assertEqual(correct_answer[0], 6)
        remove_everything_from_test_user_db()

    def test_getting_number_of_answer(self):
        remove_everything_from_test_user_db()
        fill_table()
        number_of_answer = table_questions.get_number_of_answer_with_question_id_and_position(1, 1, test_db_name)
        self.assertEqual(number_of_answer, 6)
        number_of_answer = table_questions.get_number_of_answer_with_question_id_and_position(1, 2, test_db_name)
        self.assertEqual(number_of_answer, 2)
        number_of_answer = table_questions.get_number_of_answer_with_question_id_and_position(1, 3, test_db_name)
        self.assertEqual(number_of_answer, 3)
        number_of_answer = table_questions.get_number_of_answer_with_question_id_and_position(1, 4, test_db_name)
        self.assertEqual(number_of_answer, 4)
        remove_everything_from_test_user_db()
