import json
import random
import string
import time
from locust import HttpUser, task, between, SequentialTaskSet, TaskSet

class SnackdrawerUser(HttpUser):
    wait_time = between(1,3)
    def on_start(self):
        self.username = get_random_string()
        self.password = get_random_string()
        self.user_created = False
        self.snacks = None
        self.drawers = None
        self.auth_token = None

    @task(10)
    def view_snacks(self):
        response = self.client.get('/snacks/')
        self.snacks = json.loads(response.text)

    @task(1)
    def add_snack(self):
        if self.auth_token is None:
            self.login()
        
        response = self.client.post(
            '/snacks/',
            json={
                'name': get_random_string()
            },
            headers={
                'x-access-token': self.auth_token
            }
        )

        if response.status_code == 401:
            self.auth_token = None

    def login(self):
        if self.user_created is False:
            response = self.client.post(
                '/auth/users',
                json={
                    'username': self.username,
                    'password': self.password
                }
            )

            if response.status_code == 201:
                self.user_created = True
        
        if self.user_created is True:
            response = self.client.post(
                '/auth/login',
                json={
                    'username': self.username,
                    'password': self.password
                }
            )

            response = json.loads(response.text)
            self.auth_token = response['token']


def get_random_string() -> str:
    letters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(letters) for i in range(10))
    return password