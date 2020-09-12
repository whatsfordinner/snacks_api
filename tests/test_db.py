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