import jsonschema
import logging
import snackdrawer
import unittest
from snackdrawer import drawers
from snackdrawer.users import generate_jwt
from tests.test_fixtures import sqlite_db

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.app = snackdrawer.create_app()
        self.client = self.app.test_client()
        sqlite_db.purge_db()
        sqlite_db.pollute_db(self.app.config['DATABASE'])
    
    def tearDown(self):
        pass

class DrawersTestCase(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.app = snackdrawer.create_app()
        self.client = self.app.test_client()
        sqlite_db.purge_db()
        sqlite_db.pollute_db(self.app.config['DATABASE'])

    def tearDown(self):
        pass

    def test_find_by_name(self):
        with self.app.app_context():
            user_claims = {
                'user': '1',
                'role': 'user'
            }
            expect = {
                'id': 1,
                'name': 'foo'
            }
            result = drawers.find_by_name(user_claims, 'foo')

        self.assertDictEqual(expect, result)

    def test_find_by_name_nonexistent(self):
        pass

    def test_find_by_name_other_user(self):
        pass

    def test_find_by_id(self):
        pass

    def test_find_by_id_nonexistent(self):
        pass

    def test_find_by_id_other_user(self):
        pass

    def test_get_user_drawers(self):
        pass

    def test_get_user_drawers_no_drawers(self):
        pass

    def test_get_contents(self):
        pass

    def test_get_contents_no_contents(self):
        pass