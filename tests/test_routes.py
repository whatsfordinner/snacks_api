import logging
import snacks
import unittest
from tests.test_fixtures import sqlite_db

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.app = snacks.create_app()
        self.client = self.app.test_client()
        sqlite_db.purge_db(self.app.config['DATABASE'])
        sqlite_db.pollute_db(self.app.config['DATABASE'])

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
        sqlite_db.delete_snacks(self.app.config['DATABASE'])
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
        expect_post = {'id': 4}
        expect_get = {
            'snack': {
                'id': 4,
                'name': 'pretzels'
            }
        }
        data = {'name':'pretzels'}

        result_post = self.client.post(
            '/snacks/',
            json=data
        )
        self.assertEqual(201, result_post.status_code)
        self.assertDictEqual(expect_post, result_post.get_json())

        result_get = self.client.get('/snacks/4')
        self.assertEqual(200, result_get.status_code)
        self.assertDictEqual(expect_get, result_get.get_json())


    def test_create_nonunique_snack(self):
        data = {'name': 'chocolate'}

        result = self.client.post(
            '/snacks/',
            json=data
        )
        self.assertEqual(422, result.status_code)

    def test_invalid_data(self):
        data = {'foo': 'bar'}

        result = self.client.post(
            '/snacks/',
            json=data
        )
        self.assertEqual(400, result.status_code)