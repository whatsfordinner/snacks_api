import jsonschema
import logging
import snackdrawer
import unittest
from snackdrawer import db, drawers
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

    def test_get_drawers(self):
        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        expect = {
            'drawers': [
                {
                    'id': 1,
                    'name': 'foo'
                },
                {
                    'id': 2,
                    'name': 'bar'
                }
            ]
        }
        result = self.client.get(
            '/drawers/',
            headers={
                'x-access-token': access_token
            })

        self.assertEqual(200, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_get_drawer(self):
        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        expect = {
            'drawer': {
                'id': 1,
                'name': 'foo',
                'contents': [
                    {
                        'id': 1,
                        'name': 'chips'
                    },
                    {
                        'id': 3,
                        'name': 'cookies'
                    }
                ]
            }
        }
        result = self.client.get(
            '/drawers/1',
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(200, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_get_drawer_invalid(self):
        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        result = self.client.get(
            '/drawers/0',
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(400, result.status_code)

    def test_get_drawer_nonexistent(self):
        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        result = self.client.get(
            '/drawers/8',
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(404, result.status_code)

    def test_get_drawer_other_user(self):
        access_token = generate_jwt(2, self.app.config['SECRET_KEY']).decode('UTF-8')
        result = self.client.get(
            '/drawers/1',
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(404, result.status_code)

    def test_new_drawer(self):
        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {
            'name': 'baz'
        }
        expect = {
            'drawer': {
                'id': 3,
                'name': 'baz',
                'contents': []
            }
        }
        result = self.client.post(
            '/drawers/',
            json=data,
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(201, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_new_drawer_already_exists(self):
        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {
            'name': 'foo'
        }
        result = self.client.post(
            '/drawers/',
            json=data,
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(422, result.status_code)

    def test_new_drawer_already_exists_for_other_user(self):
        access_token = generate_jwt(2, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {
            'name': 'foo'
        }
        expect = {
            'drawer': {
                'id': 3,
                'name': 'foo',
                'contents': []
            }
        }
        result = self.client.post(
            '/drawers/',
            json=data,
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(201, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_new_drawer_invalid(self):
        access_token = generate_jwt(2, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {
            'foo': 'bar'
        }
        result = self.client.post(
            '/drawers/',
            json=data,
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(400, result.status_code)
    
    def test_add_snack_to_drawer(self):
        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {
            'snack': 1
        }
        check = {
            'drawer': {
                'id': 2,
                'name': 'bar',
                'contents': [
                    {
                        'id': 1,
                        'name': 'chips'
                    }
                ]
            }
        }
        result = self.client.post(
            '/drawers/2',
            json=data,
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(201, result.status_code)

        result = self.client.get(
            '/drawers/2',
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(200, result.status_code)
        self.assertDictEqual(check, result.get_json())

    def test_add_already_added_snack_to_drawer(self):
        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {
            'snack': 3
        }
        result = self.client.post(
            '/drawers/1',
            json=data,
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(422, result.status_code)

    def test_add_nonexistent_snack_to_drawer(self):
        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {
            'snack': 5
        }
        result = self.client.post(
            '/drawers/1',
            json=data,
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(422, result.status_code)

    def test_add_snack_to_nonexistent_drawer(self):
        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {
            'snack': 1
        }
        result = self.client.post(
            '/drawers/5',
            json=data,
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(404, result.status_code)

    def test_add_snack_to_drawer_not_owned(self):
        access_token = generate_jwt(2, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {
            'snack': 2
        }
        check = {
            'drawer': {
                'id': 2,
                'name': 'bar',
                'contents': []
            }
        }
        result = self.client.post(
            '/drawers/2',
            json=data,
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(404, result.status_code)

        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        result = self.client.get(
            '/drawers/2',
            headers={
                'x-access-token': access_token
            }
        )

        self.assertDictEqual(check, result.get_json())

    def test_add_snack_to_invalid_drawer(self):
        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {
            'snack': 3
        }
        result = self.client.post(
            '/drawers/0',
            json=data,
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(400, result.status_code)

    def test_add_snack_to_drawer_invalid_data(self):
        access_token = generate_jwt(1, self.app.config['SECRET_KEY']).decode('UTF-8')
        data = {
            'foo': 'bar'
        }
        result = self.client.post(
            '/drawers/2',
            json=data,
            headers={
                'x-access-token': access_token
            }
        )

        self.assertEqual(400, result.status_code)

class DrawersTestCase(unittest.TestCase):
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

    def test_find_by_id(self):
        with self.app.app_context():
            user_claims = {
                'user': '1',
                'role': 'user'
            }
            expect = {
                'id': 2,
                'name': 'bar',
                'contents': []
            }
            result = drawers.find_by_id(user_claims, 2)

        self.assertDictEqual(expect, result)

    def test_find_by_id_invalid(self):
        with self.app.app_context():
            user_claims = {
                'user': '1',
                'role': 'user'
            }

            self.assertIsNone(drawers.find_by_id(user_claims, -3))

    def test_find_by_id_nonexistent(self):
        with self.app.app_context():
            user_claims = {
                'user': '1',
                'role': 'user'
            }

            self.assertIsNone(drawers.find_by_id(user_claims, 4))

    def test_find_by_id_other_user(self):
        with self.app.app_context():
            user_claims = {
                'user': '2',
                'role': 'user'
            }

            self.assertIsNone(drawers.find_by_id(user_claims, 1))
