import json
import random
import string
import time
from locust import HttpUser, task, between, SequentialTaskSet, TaskSet
from locust.exception import RescheduleTask

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
        snacks = json.loads(response.text)
        self.snacks = snacks['snacks']

    @task(4)
    def add_snack(self):
        if self.auth_token is None:
            self.login()
        
        with self.client.post(
            '/snacks/',
            json={
                'name': get_random_string()
            },
            headers={
                'x-access-token': self.auth_token
            },
            catch_response=True
        ) as response:
            if response.status_code == 401:
                self.auth_token = None
                raise RescheduleTask()
    
    @task(3)
    def view_drawers(self):
        if self.auth_token is None:
            self.login()

        with self.client.get(
            '/drawers/',
            headers={
                'x-access-token': self.auth_token
            },
            catch_response=True
        ) as response:
            if response.status_code == 401:
                self.auth_token = None
                raise RescheduleTask()

            drawers = json.loads(response.text)
            self.drawers = drawers['drawers']

    @task(2)
    def view_drawer(self):
        if self.auth_token is None:
            self.login()

        if self.drawers is None:
            self.view_drawers()

        if len(self.drawers) == 0:
            self.create_drawer()
            self.view_drawers()

        drawer = random.choice(self.drawers)['id']
        with self.client.get(
            f'/drawers/{drawer}',
            headers={
                'x-access-token': self.auth_token
            },
            name='/drawers/:drawer_id',
            catch_response=True
        ) as response:

            if response.status_code == 401:
                self.auth_token = None
                raise RescheduleTask()

    @task(1)
    def create_drawer(self):
        if self.auth_token is None:
            self.login()
        
        drawer_name = get_random_string()
        with self.client.post(
            '/drawers/',
            json={
                'name': drawer_name
            },
            headers={
                'x-access-token': self.auth_token
            },
            catch_response=True
        ) as response:

            if response.status_code == 401:
                self.auth_token = None
                raise RescheduleTask()

    @task(3)
    def add_snack_to_drawer(self):
        if self.auth_token is None:
            self.login()
        
        if self.drawers is None:
            self.view_drawers()
        
        if len(self.drawers) == 0:
            self.create_drawer()
            self.view_drawers()

        if self.snacks is None:
            self.view_snacks()
        
        drawer = random.choice(self.drawers)['id']
        with self.client.get(
            f'/drawers/{drawer}',
            headers={
                'x-access-token': self.auth_token
            },
            name='/drawers/:drawer_id',
            catch_response=True
        ) as response:

            if response.status_code == 401:
                self.auth_token = None
                raise RescheduleTask()
            
        contents = json.loads(response.text)

        snack_id = None
        for snack in self.snacks:
            candidate = True
            for content in contents['drawer']['contents']:
                if snack['id'] == content['id']:
                    candidate = False
            
            if candidate == True:
                snack_id = snack['id']
                break

        with self.client.post(
            f'/drawers/{drawer}',
            json={
                'snack': snack_id
            },
            headers={
                'x-access-token': self.auth_token
            },
            name='/drawers/:drawer_id',
            catch_response=True
        ) as result:

            if result.status_code == 401:
                self.auth_token = None
                raise RescheduleTask()

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
    return ''.join(random.choice(letters) for i in range(10))