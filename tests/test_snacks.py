import jsonschema
import logging
import snackdrawer
import unittest
from snackdrawer import db,snacks
from snackdrawer.users import generate_jwt
from tests.test_fixtures import sqlite_db

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.app = snackdrawer.create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.get_db().drop_db()
            db.get_db().init_db()
        sqlite_db.populate_db(f'sqlite:///{self.app.config["DATABASE"]}')

    def tearDown(self):
        pass

    def test_get_snacks(self):
        expect = {
            'snacks': [
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
        }

        result = self.client.get('/snacks/')
        self.assertEqual(200, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_get_empty_snacks(self):
        sqlite_db.delete_snacks(f'sqlite:///{self.app.config["DATABASE"]}')
        expect = {'snacks':[]}
        
        result = self.client.get('/snacks/')
        self.assertEqual(200, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_get_snack(self):
        expect = {
            'snack': {
                'id': 3,
                'name': 'cookies'
            }
        }

        result = self.client.get('/snacks/3')
        self.assertEqual(200, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_get_nonexistent_snack(self):
        result = self.client.get('/snacks/8')
        self.assertEqual(404, result.status_code)
    
    def test_get_invalid_snackid(self):
        result = self.client.get('/snacks/0')
        self.assertEqual(400, result.status_code)

    def test_create_snack(self):
        token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        expect = {
            'snack': {
                'id': 4,
                'name': 'pretzels'
            }
        }
        data = {'name':'pretzels'}

        result_post = self.client.post(
            '/snacks/',
            json=data,
            headers={
                'x-access-token': token
            }
        )
        self.assertEqual(201, result_post.status_code)
        self.assertDictEqual(expect, result_post.get_json())

        result_get = self.client.get('/snacks/4')
        self.assertEqual(200, result_get.status_code)
        self.assertDictEqual(expect, result_get.get_json())

    def test_create_nonunique_snack(self):
        token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {'name': 'chocolate'}

        result = self.client.post(
            '/snacks/',
            json=data,
            headers={
                'x-access-token': token
            }
        )
        self.assertEqual(422, result.status_code)

    def test_invalid_data(self):
        token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {'foo': 'bar'}

        result = self.client.post(
            '/snacks/',
            json=data,
            headers={
                'x-access-token': token
            }
        )
        self.assertEqual(400, result.status_code)

    def test_create_no_jwt(self):
        data = {'name':'pretzels'}

        result_post = self.client.post(
            '/snacks/',
            json=data
        )
        self.assertEqual(401, result_post.status_code)

class SnacksTestCase(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.app = snackdrawer.create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.get_db().drop_db()
            db.get_db().init_db()
        sqlite_db.populate_db(f'sqlite:///{self.app.config["DATABASE"]}')

    def tearDown(self):
        pass

    def test_to_db(self):
        with self.app.app_context():
            data = {
                'name': 'pretzels'
            }
            expect = {
                'id': 4,
                'name': 'pretzels'
            }
            result = snacks.to_db(data)

            self.assertEqual(expect, result)
            self.assertEqual(result, db.get_db().get_snack(snack_id=result['id']))

    def test_to_db_already_exists(self):
        with self.app.app_context():
            data = {
                'name': 'cookies'
            }

            with self.assertRaises(ValueError):
                snacks.to_db(data)

    def test_to_db_invalid_data(self):
        with self.app.app_context():
            data = {
                'foo': 'bar'
            }

            with self.assertRaises(jsonschema.ValidationError):
                snacks.to_db(data)