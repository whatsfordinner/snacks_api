import beeline
import logging
import pugsql
from flask import current_app, g
from snackdrawer.prometheus import time_db

def get_db():
    if 'db' not in g:
        g.db = SnackdrawerDB(
            'snackdrawer/queries',
            f'sqlite:///{current_app.config["DATABASE"]}'
        )
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.disconnect()

def init_db(app):
    db = SnackdrawerDB(
        'snackdrawer/queries',
        f'sqlite:///{app.config["DATABASE"]}'
    )
    db.init_db()
    db.disconnect()

def init_app(app):
    app.teardown_appcontext(close_db)

class SnackdrawerDB():
    # pylint: disable=no-member
    @beeline.traced(name='connecting_to_db')
    def __init__(self, query_dir, connection_string):
        self.db = pugsql.module(query_dir)
        self.db.connect(connection_string)

    @beeline.traced(name='disconnecting_from_db')
    def disconnect(self) -> None:
        self.db.disconnect()

    def init_db(self) -> None:
        self.db.create_snacks()
        self.db.create_users()
        self.db.create_drawers()
        self.db.create_drawercontents()
    
    def drop_db(self) -> None:
        self.db.drop_snacks()
        self.db.drop_users()
        self.db.drop_drawers()
        self.db.drop_drawercontents()

    @time_db
    def get_snacks(self) -> list:
        snacks = []
        result = self.db.get_snacks()
        for row in result:
            snacks.append(row)
        
        return snacks
    
    @time_db
    def get_snack(self, snack_id: int=None, snack_name: str=None) -> dict:
        if snack_id is not None:
            return self.db.get_snack(snack_id=snack_id)
        elif snack_name is not None:
            return self.db.get_snack_by_name(snack_name=snack_name)
        else:
            return None

    @time_db
    def add_snack(self, snack_name: str) -> int:
        return self.db.insert_snack(snack_name=snack_name)

    @time_db
    def get_user(self, user_id: int=None, username: str=None, hash: bool=False) -> dict:
        if user_id is not None:
            if hash:
                return self.db.get_user(user_id=user_id)
            else:
                return self.db.get_user_no_hash(user_id=user_id)
        elif username is not None:
            if hash:
                return self.db.get_user_by_username(username=username)
            else:
                return self.db.get_user_by_username_no_hash(username=username)

    @time_db
    def add_user(self, username: str, password_hash: str) -> int:
        return self.db.insert_user(username=username, password_hash=password_hash)

    @time_db
    def get_drawers(self, user_id: int=None, drawer_name: str=None) -> list:
        drawers = []
        if user_id is not None:
            result = self.db.get_drawers_by_userid(user_id=user_id)
        elif drawer_name is not None:
            result = self.db.get_drawers_by_name(drawer_name=drawer_name)
        else:
            result = self.db.get_drawers()
        
        for row in result:
            drawers.append(row)
        
        return drawers

    @time_db
    def get_drawer(self, user_id: int, drawer_id: int=None, drawer_name: str=None) -> dict:
        if drawer_id is not None:
            return self.db.get_drawer_by_id_and_userid(user_id=user_id, drawer_id=drawer_id)
        elif drawer_name is not None:
            return self.db.get_drawer_by_name_and_userid(user_id=user_id, drawer_name=drawer_name)
        else:
            return None

    def add_drawer(self, user_id: int, drawer_name: str) -> int:
        return self.db.create_new_drawer(user_id=user_id, drawer_name=drawer_name)

    @time_db
    def get_drawer_snacks(self, drawer_id: int) -> list:
        snacks = []
        result = self.db.get_snacks_in_drawer(drawer_id=drawer_id)
        for row in result:
            snacks.append(row)

        return snacks

    @time_db
    def add_snack_to_drawer(self, drawer_id: int, snack_id: int) -> int:
        self.db.add_snack_to_drawer(drawer_id=drawer_id, snack_id=snack_id)