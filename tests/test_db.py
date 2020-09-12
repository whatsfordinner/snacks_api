import logging
import os
import unittest
from snackdrawer import db
from tests.test_fixtures import sqlite_db

class DBTestCase(unittest.TestCase):
    def setUp(self):
        connection_string = f'sqlite:///{os.getcwd()}/tests/test.sqlite'
        logging.disable(logging.CRITICAL)
        self.db = db.SnackdrawerDB(
            'snackdrawer/queries/',
            connection_string
        )
        self.db.drop_db()
        self.db.init_db()
        sqlite_db.populate_db(connection_string)

    def tearDown(self):
        self.db.disconnect()
    
    def test_get_snacks(self):
        expect = [
            {
                'id': 1,
                'name': 'chips'
            },
            {
                'id': 2,
                'name': 'chocolate'
            },
            {
                'id': 3,
                'name': 'cookies'
            }
        ]
        result = self.db.get_snacks()
        self.assertListEqual(expect, result)

    def test_get_snack_by_id(self):
        expect = {
            'id': 2,
            'name': 'chocolate'
        }
        result = self.db.get_snack(snack_id=2)
        self.assertDictEqual(expect, result)

    def test_get_snack_by_id_nonexistent(self):
        self.assertIsNone(self.db.get_snack(snack_id=5))
    
    def test_get_snack_by_name(self):
        expect = {
            'id': 3,
            'name': 'cookies'
        }
        result = self.db.get_snack(snack_name='cookies')
        self.assertDictEqual(expect, result)

    def test_get_snack_by_name_nonexistent(self):
        self.assertIsNone(self.db.get_snack(snack_name='foobar'))
    
    def test_get_snack_none(self):
        self.assertIsNone(self.db.get_snack())
    
    def test_add_snack(self):
        expect = {
            'id': 4,
            'name': 'pretzels'
        }
        insert_id = self.db.add_snack('pretzels')
        result = self.db.get_snack(snack_id=insert_id)
        self.assertDictEqual(expect, result)

    def test_get_user_by_id(self):
        expect = {
            'id': 1,
            'username': 'foobar',
            'password_hash': '$6$rounds=656000$DA2b7/HB7pXEwOUS$jW9EAxnXxG6Oj6prBoXh8p2dJNQYSKGgRu5xaYf6Z49bITqcF3/Yzf0YAjmpjTLPOErXyq7PZ6HLDprxhBO3s1'
        }
        result = self.db.get_user(user_id=1, hash=True)
        self.assertDictEqual(expect, result)

        expect.pop('password_hash')
        result = self.db.get_user(user_id=1)
        self.assertDictEqual(expect, result)

    def test_get_user_by_id_nonexistent(self):
        self.assertIsNone(self.db.get_user(user_id=3))
    
    def test_get_user_by_username(self):
        expect = {
            'id': 1,
            'username': 'foobar',
            'password_hash': '$6$rounds=656000$DA2b7/HB7pXEwOUS$jW9EAxnXxG6Oj6prBoXh8p2dJNQYSKGgRu5xaYf6Z49bITqcF3/Yzf0YAjmpjTLPOErXyq7PZ6HLDprxhBO3s1'
        }
        result = self.db.get_user(username='foobar', hash=True)
        self.assertDictEqual(expect, result)

        expect.pop('password_hash')
        result = self.db.get_user(username='foobar')
        self.assertDictEqual(expect, result)

    def test_get_user_by_username_nonexistent(self):
        self.assertIsNone(self.db.get_user(username='fakename'))

    def test_insert_user(self):
        expect = {
            'id': 3,
            'username': 'newbie',
            'password_hash': 'areallylonghash'
        }
        insert_id = self.db.add_user('newbie', 'areallylonghash')
        result = self.db.get_user(user_id=insert_id, hash=True)
        self.assertDictEqual(expect, result)

    def test_get_drawers(self):
        expect = [
            {
                'id': 1,
                'name': 'foo',
                'userid': 1
            },
            {
                'id': 2,
                'name': 'bar',
                'userid': 1
            }
        ]
        result = self.db.get_drawers()
        self.assertListEqual(expect, result)

    def test_get_drawers_by_userid(self):
        expect = [
            {
                'id': 1,
                'name': 'foo',
                'userid': 1
            },
            {
                'id': 2,
                'name': 'bar',
                'userid': 1
            }
        ]
        result = self.db.get_drawers(user_id=1)
        self.assertListEqual(expect, result)

    def test_get_drawers_by_userid_no_drawers(self):
        expect = []
        result = self.db.get_drawers(user_id=2)
        self.assertListEqual(expect, result)
    
    def test_get_drawers_by_name(self):
        expect = [
            {
                'id': 2,
                'name': 'bar',
                'userid': 1
            }
        ]
        result = self.db.get_drawers(drawer_name='bar')
        self.assertListEqual(expect, result)
    
    def test_get_drawers_by_name_nonexistent(self):
        expect = []
        result = self.db.get_drawers(drawer_name='nobodyhere')
        self.assertListEqual(expect, result)

    def test_get_drawer_by_id(self):
        expect = {
            'id': 1,
            'name': 'foo'
        }
        result = self.db.get_drawer(1, drawer_id=1)
        self.assertDictEqual(expect, result)

    def test_get_drawer_by_id_nonexistent(self):
        self.assertIsNone(self.db.get_drawer(1, drawer_id=5))
    
    def test_get_drawer_by_id_other_drawer(self):
        self.assertIsNone(self.db.get_drawer(2, drawer_id=1))

    def test_get_drawer_by_name(self):
        expect = {
            'id': 2,
            'name': 'bar'
        }
        result = self.db.get_drawer(1, drawer_name='bar')
        self.assertDictEqual(expect, result)

    def test_get_drawer_by_name_nonexistent(self):
        self.assertIsNone(self.db.get_drawer(1, drawer_name='nobodyhere'))

    def test_get_drawer_by_name_other(self):
        self.assertIsNone(self.db.get_drawer(2, drawer_name='foo'))

    def test_get_drawer_none(self):
        self.assertIsNone(self.db.get_drawer(1))

    def test_get_drawer_snacks(self):
        expect = [
            {
                'id': 1,
                'name': 'chips'
            },
            {
                'id': 3,
                'name': 'cookies'
            }
        ]
        result = self.db.get_drawer_snacks(1)
        self.assertListEqual(expect, result)

    def test_get_drawer_snacks_empty(self):
        expect = []
        result = self.db.get_drawer_snacks(2)
        self.assertListEqual(expect, result)

    def test_get_drawer_snacks_nonexistent(self):
        expect = []
        result = self.db.get_drawer_snacks(4)
        self.assertListEqual(expect, result)

    def test_add_snack_to_drawer(self):
        expect = [
            {
                'id': 2,
                'name': 'chocolate'
            }
        ]
        self.db.add_snack_to_drawer(2, 2)
        result = self.db.get_drawer_snacks(2)
        self.assertListEqual(expect, result)