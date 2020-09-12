import jsonschema
from flask import abort, Blueprint, current_app, jsonify, make_response, request
from snackdrawer import db, snacks
from snackdrawer.users import jwt_required
from snackdrawer.validate import validate_data
from snackdrawer.prometheus import time_request, db_histogram

bp = Blueprint('drawers', __name__, url_prefix='/drawers')

@bp.route('/', methods=['GET'])
@time_request
@jwt_required
def get_drawers(user_claims: dict) -> list:
    results = db.get_db().get_drawers(user_id=user_claims['user'])
    return make_response(
        jsonify(drawers=results),
        200
    )

@bp.route('/<int:drawer_id>', methods=['GET'])
@time_request
@jwt_required
def get_drawer(user_claims: dict, drawer_id: int) -> dict:
    if drawer_id < 1:
        abort(400, 'drawer ID must be >= 1')
    
    result = find_by_id(user_claims, drawer_id)

    if result is None:
        abort(404, f'drawer with ID == {drawer_id} not found')
    
    return make_response(
        jsonify(drawer=result),
        200
    )

@bp.route('/', methods=['POST'])
@time_request
@jwt_required
def new_drawer(user_claims: dict) -> dict:
    try:
        user_id = int(user_claims['user'])
        request_data = request.get_json()
        validate_data('new_drawer', request_data)
        drawer_name = request_data['name']
        if db.get_db().get_drawer(user_id, drawer_name=request_data['name']) is None:
            new_id = db.get_db().add_drawer(user_id=user_id, drawer_name=drawer_name)
            new_drawer = find_by_id(user_claims, new_id)
        else:
            raise ValueError(f'drawer with name {drawer_name} already exists for this user')
    except ValueError as err:
        abort(422, description=err)
    
    except jsonschema.ValidationError as err:
        abort(400, err.message)
        
    return make_response(
        jsonify(drawer=new_drawer),
        201
    )

@bp.route('/<int:drawer_id>', methods=['POST'])
@time_request
@jwt_required
def add_snack_to_drawer(user_claims: dict, drawer_id: int) -> dict:
    if drawer_id < 1:
        abort(400, 'drawer ID must be >= 1')
    try:
        request_data = request.get_json()
        validate_data('add_snack_to_drawer', request_data)

        drawer = find_by_id(user_claims, drawer_id)
        if drawer is None:
            raise abort(404, description=f'drawer with ID {drawer_id} does not exist')

        snack_id = request_data['snack']
        snack = db.get_db().get_snack(snack_id=snack_id)
        if snack is None:
            raise ValueError(f'snack with ID {snack_id} does not exist')
        for content in db.get_db().get_drawer_snacks(drawer_id):
            if snack_id == content['id']:
                raise ValueError(f'snack with ID {snack_id} already exists in drawer with ID {drawer_id}')

        db.get_db().add_snack_to_drawer(drawer_id=drawer_id, snack_id=snack_id)

    except ValueError as err:
        abort(422, description=err)

    except jsonschema.ValidationError as err:
        abort(400, description=err.message)

    return make_response(
        jsonify(message='snack added to drawer'),
        201
    )

def find_by_id(user_claims: dict, id: int) -> dict:
    user_id = int(user_claims['user'])
    drawer = db.get_db().get_drawer(user_id, drawer_id=id)

    if drawer is None:
        return None
    else:
        contents = db.get_db().get_drawer_snacks(drawer['id'])
        drawer['contents'] = contents
        return drawer
