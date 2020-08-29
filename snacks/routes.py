import json
import jsonschema
from flask import abort, Blueprint, current_app, jsonify, make_response, request
from snacks import db

bp = Blueprint('snacks', __name__, url_prefix='/snacks')

@bp.route('/', methods=['GET'])
def get_snacks() -> dict:
    snacks = []
    results = db.get_db().get_snacks()

    for result in results:
        snacks.append(result)
    
    return make_response(
        jsonify(snacks=snacks),
        200
    )

@bp.route('/<int:snack_id>', methods=['GET'])
def get_snack(snack_id: int) -> dict:
    if snack_id < 1:
        abort(400, 'snack ID must be >= 1')

    result = db.get_db().get_snack(snack_id=snack_id)

    if result is None:
        abort(404, f'snack with ID == {snack_id} not found')
    
    return make_response(
        jsonify(snack=result),
        200
    )

@bp.route('/', methods=['POST'])
def new_snack() -> dict:
    try:
        request_data = request.get_json()
        validate_data('new_snack', request_data)
        validate_unique_name(request_data['name'])
        current_app.logger.info(f'adding new snack with name: {request_data["name"]}')
        result = db.get_db().insert_snack(snack_name=request_data['name'])
        current_app.logger.debug(result)
    
    except ValueError as err:
        abort(422, description=err)
    
    except jsonschema.ValidationError as err:
        abort(400, err.message)
    
    return make_response(
        jsonify(id=result),
        201)


def get_schema(schema_name: str) -> dict:
    schema_file_location = f'snacks/schemas/{schema_name}.json'
    current_app.logger.debug(f'reading in schema file: {schema_file_location}')
    with open(schema_file_location, 'r') as schema_file:
        schema_json = json.load(schema_file)
    return schema_json

def validate_data(schema_name: str, request_data: dict) -> None:
    schema = get_schema(schema_name)
    jsonschema.validate(request_data, schema)

def validate_unique_name(snack_name: str) -> None:
    if db.get_db().get_snack_by_name(snack_name=snack_name) is not None:
        raise ValueError(f'snack with name {snack_name} already exists')