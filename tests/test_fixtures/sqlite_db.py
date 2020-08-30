import pugsql
import snackdrawer
from snackdrawer import db

def purge_db():
    app = snackdrawer.create_app()
    with app.app_context():
        db.get_db().drop_snacks()
        db.get_db().drop_users()
        db.get_db().drop_drawers()
        db.get_db().drop_drawercontents()

def pollute_db(database):
    app = snackdrawer.create_app()
    with app.app_context():
        db.get_db().create_snacks()
        db.get_db().create_users()
        db.get_db().create_drawers()
        db.get_db().create_drawercontents()
    
    connection = pugsql.module('tests/test_fixtures/queries/')
    connection.connect(f'sqlite:///{database}')
    connection.populate_snacks()

def delete_snacks():
    app = snackdrawer.create_app()
    with app.app_context():
        db.get_db().delete_all_snacks()