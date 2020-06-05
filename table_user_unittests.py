import sqlite3
import unittest

import table_user


def remove_everything_from_test_user_db():
    test_db_name = 'disney_bot_test.db'
    conn = sqlite3.connect(test_db_name)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM users""").fetchall()
    conn.commit()


class TestTableUser(unittest.TestCase):

    def test_changing_name(self):
        test_db_name = 'disney_bot_test.db'
        nick = 'Leonardo da Vinci'
        vk_id = 123456
        user = (nick, vk_id,)
        self.assertTrue(table_user.insert_new_user(user, test_db_name))  # add some user
        new_nick = 'Leonardo'
        self.assertTrue(table_user.change_nick(vk_id, new_nick, test_db_name))  # change name to existing user
        bad_vk_id = 111
        self.assertFalse(table_user.change_nick(bad_vk_id, new_nick, test_db_name))  # change name to nonexistent user
        remove_everything_from_test_user_db()

    def test_inserting_new_user(self):
        test_db_name = 'disney_bot_test.db'
        nick = 'Leonardo da Vinci'
        vk_id = 123456
        user = (nick, vk_id, )
        self.assertTrue(table_user.insert_new_user(user, test_db_name))  # new user
        self.assertFalse(table_user.insert_new_user(user, test_db_name))  # user with a same vk_id and name
        nick = 'Leonardo'
        user = (nick, vk_id, )
        self.assertFalse(table_user.insert_new_user(user, test_db_name))  # user with a same vk_id
        vk_id = 123457
        user = (nick, vk_id,)
        self.assertTrue(table_user.insert_new_user(user, test_db_name))  # user with a new info
        vk_id = 123458
        user = (nick, vk_id,)
        self.assertTrue(table_user.insert_new_user(user, test_db_name))  # user with a same name, but new vk_id
        remove_everything_from_test_user_db()
