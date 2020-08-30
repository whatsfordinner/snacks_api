from passlib.apps import custom_app_context
from snackdrawer import db

def find_by_username(username: str) -> dict:
    return db.get_db().get_user_by_username(username=username)

def find_by_userid(id: int) -> dict:
    return db.get_db().get_user(user_id=id)

def verify_credentials(username: str, password: str) -> dict:
    claimed_user = find_by_username(username)

    if claimed_user is None:
        raise ValueError(f'username or password incorrect')

    if custom_app_context.verify(password, claimed_user["password_hash"]):
        return claimed_user
    else:
        return ValueError('username or password incorrect')

def new_user(username: str, password: str) -> dict:
    if find_by_username(username) is None:
        password_hash = custom_app_context.encrypt(password)
        id = db.get_db().insert_user(username=username, password_hash=password_hash)
        return find_by_userid(id)
    else:
        return ValueError('username taken')
    
def generate_jwt():
    pass

def validate_jwt():
    pass