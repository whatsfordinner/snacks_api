import datetime
import jsonschema
import jwt
import logging
import snackdrawer
import unittest
from flask import jsonify, make_response
from snackdrawer import db, users
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

    def test_new_user(self):
        data = {
            'username': 'cookiemonster',
            'password': 'lovecookies'
        }
        expect = {
            'id': 3,
            'username': 'cookiemonster'
        }
        result = self.client.post(
            '/auth/users',
            json=data
        )

        self.assertEqual(201, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_new_user_existing(self):
        data = {
            'username': 'foobar',
            'password': 'sneaky'
        }
        result = self.client.post(
            '/auth/users',
            json=data
        )

        self.assertEqual(422, result.status_code)

    def test_new_user_invalid(self):
        data = {
            'foo': 'bar'
        }
        result = self.client.post(
            '/auth/users',
            json=data
        )

        self.assertEqual(400, result.status_code)

    def test_validate_user(self):
        data = {
            'username': 'foobar',
            'password': 'qux'
        }
        result = self.client.post(
            '/auth/login',
            json=data
        )
        jwt_payload = result.get_json()['token']
        jwt_payload = jwt.decode(
            jwt_payload,
            'tasty_snacks',
            audience='snackdrawer',
            algorithms=['HS256']
        )

        self.assertEqual(201, result.status_code)
        self.assertEqual('1', jwt_payload['user'])

    def test_validate_user_nonexistent(self):
        data = {
            'username': 'beetles',
            'password': 'notimportant'
        }
        result = self.client.post(
            '/auth/login',
            json=data
        )

        self.assertEqual(401, result.status_code)

    def test_validate_user_bad_creds(self):
        data = {
            'username': 'foobar',
            'password': 'wrongpass'
        }
        result = self.client.post(
            '/auth/login',
            json=data
        )

        self.assertEqual(401, result.status_code)

    def test_validate_user_invalid(self):
        data = {
            'foo': 'bar'
        }
        result = self.client.post(
            '/auth/login',
            json=data
        )

        self.assertEqual(400, result.status_code)

class UsersTestCase(unittest.TestCase):
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

    def test_verify_credentials(self):
        with self.app.app_context():
            data = {
                'username': 'foobar',
                'password': 'qux'
            }
            expect = {
                'id': 1,
                'username': 'foobar'
            }
            result = users.verify_credentials(data)
        
        self.assertDictEqual(expect, result)

    def test_verify_credentials_invalid(self):
        with self.app.app_context():
            data = {
                'foo': 'bar'
            }
            
            with self.assertRaises(jsonschema.ValidationError):
                users.verify_credentials(data)

    def test_verify_credentials_nonexistent(self):
        with self.app.app_context():
            data = {
                'username': 'beetles',
                'password': 'bugsrule'
            }

            with self.assertRaises(ValueError):
                users.verify_credentials(data)

    def test_verify_credentials_bad(self):
        with self.app.app_context():
            data = {
                'username': 'foobar',
                'password': 'xyzzy'
            }

            with self.assertRaises(ValueError):
                users.verify_credentials(data)
    
    def test_add_new_user(self):
        with self.app.app_context():
            data = {
                'username': 'cookiemonster',
                'password': 'lovecookies'
            }
            expect = {
                'id': 3,
                'username': 'cookiemonster'
            }
            result = users.add_new_user(data)

        self.assertDictEqual(expect, result)

    def test_add_new_user_invalid(self):
        with self.app.app_context():
            data = {
                'foo': 'bar'
            }

            with self.assertRaises(jsonschema.ValidationError):
                users.add_new_user(data)

    def test_add_new_user_existing(self):
        with self.app.app_context():
            data = {
                'username': 'foobar',
                'password': 'doesnotmatter'
            }

            with self.assertRaises(ValueError):
                users.add_new_user(data)

    def test_generate_jwt(self):
        result = users.generate_jwt(5, 'secret')
        decoded = jwt.decode(result, 'secret', audience='snackdrawer', algorithms=['HS256'])

        self.assertEqual(5, int(decoded['user']))

    def test_validate_jwt(self):
        with self.app.app_context():
            data = jwt.encode(
                {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
                    'iat': datetime.datetime.utcnow(),
                    'aud': 'snackdrawer',
                    'user': 1,
                    'role': 'user'
                },
                'secret',
                algorithm='HS256'
            )
            expect = {
                'user': 1,
                'role': 'user'
            }
            result = users.validate_jwt(data, 'secret')
        
        self.assertDictEqual(expect, result)
        

    def test_validate_jwt_invalid(self):
        with self.app.app_context():
            data = jwt.encode(
                {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
                    'iat': datetime.datetime.utcnow(),
                    'aud': 'snackdrawer',
                    'user': 1,
                    'role': 'user'
                },
                'wrongsecret',
                algorithm='HS256'
            )

            with self.assertRaises(jwt.InvalidTokenError):
                users.validate_jwt(data, 'secret')
        

    def test_validate_jwt_expired(self):
        with self.app.app_context():
            data = jwt.encode(
                {
                    'exp': datetime.datetime.utcnow() - datetime.timedelta(days=1) + datetime.timedelta(seconds=30),
                    'iat': datetime.datetime.utcnow() - datetime.timedelta(days=1),
                    'aud': 'snackdrawer',
                    'user': 1,
                    'role': 'user'
                },
                'secret',
                algorithm='HS256'
            )

            with self.assertRaises(jwt.ExpiredSignature):
                users.validate_jwt(data, 'secret')
        
class JwtTestCase(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.app = snackdrawer.create_app()
        self.client = self.app.test_client()
        self.app.add_url_rule('/test','example_func', self.example_func, methods=['POST'])


    def tearDown(self):
        pass

    @staticmethod
    @users.jwt_required
    def example_func(user):
        return make_response(
            jsonify(user),
            200
        )

    def test_jwt_required(self):
        token = users.generate_jwt(1, self.app.config['SECRET_KEY'])
        token = token.decode('UTF-8')
        expect = {
            'user': 1,
            'role': 'user'
        }
        result = self.client.post(
            '/test',
            headers={
                'x-access-token': token
            }
        )

        self.assertEqual(200, result.status_code)
        self.assertDictEqual(expect, result.get_json())

    def test_jwt_required_no_jwt(self):
        result = self.client.post('/test')

        self.assertEqual(401, result.status_code)

    def test_jwt_required_invalid_jwt(self):
        token = 'totallyfaketoken'
        result = self.client.post(
            '/test',
            headers={
                'x-access-token': token
            }
        )

        self.assertEqual(401, result.status_code)