import sqlite3
import unittest

import table_records
import table_user


def remove_everything_from_test_user_db():
    test_db_name = 'disney_bot_test.db'
    conn = sqlite3.connect(test_db_name)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM records""")
    cursor.execute("""DELETE FROM users""")
    conn.commit()


class TestTableRecords(unittest.TestCase):

    def test_changing_record(self):
        test_db_name = 'disney_bot_test.db'
        new_record = 1
        nick = 'Leonardo da Vinci'
        vk_id = 123456
        user = (nick, vk_id,)
        self.assertFalse(table_records.change_record(vk_id, new_record, test_db_name))  # nonexistent user
        self.assertTrue(table_user.insert_new_user(user, test_db_name))
        self.assertFalse(table_records.change_record(vk_id, new_record, test_db_name))  # record is not exist
        self.assertTrue(table_records.insert_new_record(vk_id, new_record, test_db_name))
        self.assertTrue(table_records.change_record(vk_id, new_record, test_db_name))  # everything is fine
        new_record = 2
        self.assertTrue(table_records.change_record(vk_id, new_record, test_db_name))  # everything is fine again
        new_record = 1
        self.assertTrue(table_records.change_record(vk_id, new_record, test_db_name))  # everything is fine again
        remove_everything_from_test_user_db()

    def test_inserting_new_record(self):
        test_db_name = 'disney_bot_test.db'
        new_record = 1
        vk_id = 123456
        self.assertTrue(table_records.insert_new_record(vk_id, new_record, test_db_name))
        self.assertFalse(table_records.insert_new_record(vk_id, new_record, test_db_name))
        new_record = 2
        self.assertTrue(table_records.insert_new_record(vk_id, new_record, test_db_name))
        new_record = 1
        self.assertFalse(table_records.insert_new_record(vk_id, new_record, test_db_name))
        remove_everything_from_test_user_db()

    def test_getting_all_records(self):
        test_db_name = 'disney_bot_test.db'
        new_record = 1
        vk_id = 1
        self.assertTrue(table_records.insert_new_record(vk_id, new_record, test_db_name))
        new_record = 2
        vk_id = 2
        self.assertTrue(table_records.insert_new_record(vk_id, new_record, test_db_name))
        new_record = 3
        vk_id = 3
        self.assertTrue(table_records.insert_new_record(vk_id, new_record, test_db_name))
        records = table_records.get_all_records(test_db_name)
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0][1], 1)
        self.assertEqual(records[0][2], 1)
        self.assertEqual(records[1][1], 2)
        self.assertEqual(records[1][2], 2)
        self.assertEqual(records[2][1], 3)
        self.assertEqual(records[2][2], 3)
        remove_everything_from_test_user_db()

    def test_getting_record_with_user_id(self):
        test_db_name = 'disney_bot_test.db'
        new_record = 1
        vk_id = 1
        self.assertEqual(table_records.get_record_with_user_id(vk_id, test_db_name), -1)    # nonexistent user
        self.assertTrue(table_records.insert_new_record(vk_id, new_record, test_db_name))   # add user
        self.assertEqual(table_records.get_record_with_user_id(vk_id, test_db_name), 1)     # correct record
        self.assertNotEqual(table_records.get_record_with_user_id(vk_id, test_db_name), 2)  # incorrect record
        remove_everything_from_test_user_db()
