import pugsql

def purge_db(database):
    db = pugsql.module('tests/test_fixtures/queries')
    db.connect(f'sqlite:///{database}')
    db.purge_snacks()

def pollute_db(database):
    db = pugsql.module('tests/test_fixtures/queries')
    db.connect(f'sqlite:///{database}')
    db.create_snacks()
    db.populate_snacks()

def delete_snacks(database):
    db = pugsql.module('tests/test_fixtures/queries')
    db.connect(f'sqlite:///{database}')
    db.delete_snacks()