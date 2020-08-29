import logging
import pugsql
from flask import current_app, g

def get_db():
    if 'db' not in g:
        conn = pugsql.module('snacks/queries/')
        conn.connect(f'sqlite:///{current_app.config["DATABASE"]}')
        g.db = conn
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.disconnect()

def init_db(app):
    db = pugsql.module('snacks/queries/')
    db.connect(f'sqlite:///{app.config["DATABASE"]}')
    db.create_snacks()
    db.disconnect()

def init_app(app):
    app.teardown_appcontext(close_db)