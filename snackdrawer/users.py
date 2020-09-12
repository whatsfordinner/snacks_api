import datetime
import json
import jsonschema
import jwt
from flask import abort, Blueprint, current_app, jsonify, make_response, request
from functools import wraps
from passlib.apps import custom_app_context
from snackdrawer import db
from snackdrawer.prometheus import time_request, time_auth, db_histogram
from snackdrawer.validate import validate_data

bp = Blueprint('users', __name__, url_prefix='/auth')

@bp.route('/users', methods=['POST'])
@time_request
def new_user() -> dict:
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
@time_request
def validate_user() -> dict:
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

@time_auth
def verify_credentials(data: dict) -> dict:
    validate_data('user_login', data)
    claimed_user = db.get_db().get_user(username=data['username'], hash=True)

    if claimed_user is None:
        raise ValueError(f'username or password incorrect')

    if custom_app_context.verify(data['password'], claimed_user['password_hash']):
        claimed_user.pop('password_hash', None)
        return claimed_user
    else:
        raise ValueError('username or password incorrect')

def add_new_user(data: dict) -> dict:
    validate_data('new_user', data)
    if db.get_db().get_user(username=data['username']) is None:
        password_hash = custom_app_context.hash(data['password'])
        with db_histogram.labels('insert_user').time():
            id = db.get_db().add_user(data['username'], password_hash)
        return db.get_db().get_user(user_id=id)
    else:
        raise ValueError('username taken')
    
@time_auth
def generate_jwt(user_id, secret):
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

@time_auth
def validate_jwt(jwt_payload, secret) -> dict:
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