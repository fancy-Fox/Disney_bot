import sqlite3
import unittest

import table_daily_quests

test_db_name = 'disney_bot_test.db'
true_db_name = 'disney_bot.db'


def remove_everything_from_test_user_db():
    conn = sqlite3.connect(test_db_name)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM daily_quests""")
    conn.commit()


class TestTableQuestions(unittest.TestCase):

    def test_getting_all_daily_quests_info(self):
        remove_everything_from_test_user_db()
        table_daily_quests.get_all_daily_quest_info()
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
