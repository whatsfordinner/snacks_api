# pylint: disable=no-member
import pugsql
import snackdrawer
from snackdrawer import db

def delete_snacks(connection_string):
    connection = pugsql.module('tests/test_fixtures/queries/')
    connection.connect(connection_string)
    connection.delete_all_snacks()

def populate_db(connection_string):
    connection = pugsql.module('tests/test_fixtures/queries/')
    connection.connect(connection_string)
    connection.populate_snacks()
    connection.populate_users()
    connection.populate_drawers()
    connection.populate_drawercontents()
