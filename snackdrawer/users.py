import datetime
import json
import jsonschema
import jwt
from flask import abort, Blueprint, current_app, jsonify, make_response, request
from functools import wraps
from passlib.apps import custom_app_context
from snackdrawer import db
from snackdrawer.prometheus import auth_summary, request_summary, db_summary
from snackdrawer.validate import validate_data

bp = Blueprint('users', __name__, url_prefix='/auth')

@bp.route('/users', methods=['POST'])
def new_user() -> dict:
    with request_summary.labels(request.url_rule, request.method).time():
        try:
            request_data = request.get_json()
            result = add_new_user(request_data)
        
        except ValueError as err:
            abort(422, description=err)
        
        except jsonschema.ValidationError as err:
            abort(400, err.message)

        return make_response(
            jsonify(
                id=result['id'],
                username=result['username']
            ),
            201
        )

@bp.route('/login', methods=['POST'])
def validate_user() -> dict:
    with request_summary.labels(request.url_rule, request.method).time():
        try:
            request_data = request.get_json()
            user = verify_credentials(request_data)
            new_jwt = generate_jwt(user['id'], current_app.config['SECRET_KEY'])

        except ValueError as err:
            abort(401, description=err)
        
        except jsonschema.ValidationError as err:
            abort(400, description=err.message)
        
        return make_response(
            jsonify(token=new_jwt.decode('UTF-8')),
            201
        )
    

def find_by_username(username: str, include_hash=False) -> dict:
    if include_hash:
        with db_summary.labels('get_user_by_username').time():
            return db.get_db().get_user_by_username(username=username)
    with db_summary.labels('get_user_by_username_no_hash').time():
        return db.get_db().get_user_by_username_no_hash(username=username)

def find_by_userid(id: int, include_hash=False) -> dict:
    if include_hash:
        with db_summary.labels('get_user_by_userid').time():
            return db.get_db().get_user(user_id=id)
    with db_summary.labels('get_user_by_userid_no_hash').time():
        return db.get_db().get_user_no_hash(user_id=id)

def verify_credentials(data: dict) -> dict:
    validate_data('user_login', data)
    claimed_user = find_by_username(data['username'], include_hash=True)

    if claimed_user is None:
        raise ValueError(f'username or password incorrect')

    with auth_summary.labels('verify_credentials').time():
        if custom_app_context.verify(data['password'], claimed_user['password_hash']):
            claimed_user.pop('password_hash', None)
            return claimed_user
        else:
            raise ValueError('username or password incorrect')

def add_new_user(data: dict) -> dict:
    validate_data('new_user', data)
    if find_by_username(data['username']) is None:
        password_hash = custom_app_context.hash(data['password'])
        with db_summary.labels('insert_user').time():
            id = db.get_db().insert_user(username=data['username'], password_hash=password_hash)
        return find_by_userid(id)
    else:
        raise ValueError('username taken')
    
def generate_jwt(user_id, secret):
    with auth_summary.labels('generate_jwt').time():
        jwt_payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            'iat': datetime.datetime.utcnow(),
            'aud': 'snackdrawer',
            'user': str(user_id),
            'role': 'user'
        }

        return jwt.encode(
            jwt_payload,
            secret,
            algorithm='HS256'
        )

def validate_jwt(jwt_payload, secret) -> dict:
    with auth_summary.labels('validate_jwt').time():
        decoded = jwt.decode(jwt_payload, secret, audience='snackdrawer', algorithms=['HS256'])
        return {
            'user': int(decoded['user']),
            'role': decoded['role']
        }

def jwt_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'x-access-token' not in request.headers:
            abort(401, description='no authentication token')
        
        try:
            user_claims = validate_jwt(
                request.headers['x-access-token'],
                current_app.config['SECRET_KEY']
            )
        
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            abort(401, description='invalid authentication token')

        return f(user_claims, *args, **kwargs)
    return decorator