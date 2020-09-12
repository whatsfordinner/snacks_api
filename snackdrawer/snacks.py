import jsonschema
from flask import abort, Blueprint, current_app, jsonify, make_response, request
from snackdrawer import db
from snackdrawer.prometheus import time_request, db_histogram
from snackdrawer.users import jwt_required
from snackdrawer.validate import validate_data

bp = Blueprint('snacks', __name__, url_prefix='/snacks')

@bp.route('/', methods=['GET'])
@time_request
def get_snacks() -> dict:
    results = get_all()
    return make_response(
        jsonify(snacks=results),
        200
    )

@bp.route('/<int:snack_id>', methods=['GET'])
@time_request
def get_snack(snack_id: int) -> dict:
    if snack_id < 1:
        abort(400, 'snack ID must be >= 1')

    result = find_by_id(snack_id)

    if result is None:
        abort(404, f'snack with ID == {snack_id} not found')
    
    return make_response(
        jsonify(snack=result),
        200
    )
        
@bp.route('/', methods=['POST'])
@time_request
@jwt_required
def new_snack(user_claims) -> dict:
    try:
        request_data = request.get_json()
        result = to_db(request_data)
    
    except ValueError as err:
        abort(422, description=err)
    
    except jsonschema.ValidationError as err:
        abort(400, err.message)
    
    return make_response(
        jsonify(snack=result),
        201)

def find_by_name(name: str) -> object:
    with db_histogram.labels('get_snack_by_name').time():
        return db.get_db().get_snack_by_name(snack_name=name)

def find_by_id(id: int) -> object:
    with db_histogram.labels('get_snack_by_id').time():
        return db.get_db().get_snack(snack_id=id)

def get_all() -> list:
    with db_histogram.labels('get_all_snacks').time():
        results = db.get_db().get_snacks()
    snacks = []
    for result in results:
        snacks.append(result)
    
    return snacks

def to_db(data: dict) -> dict:
    validate_data('new_snack', data)
    if find_by_name(data['name']) is None:
        with db_histogram.labels('insert_snack').time():
            id = db.get_db().insert_snack(snack_name=data['name'])
        return find_by_id(id)
    else:
        raise ValueError(f'snack with name "{data["name"]}" already exists')