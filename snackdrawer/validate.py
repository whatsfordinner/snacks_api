import json
import jsonschema
from flask import current_app

def get_schema(schema_name: str) -> dict:
    schema_file_location = f'snackdrawer/schemas/{schema_name}.json'
    current_app.logger.debug(f'reading in schema file: {schema_file_location}')
    with open(schema_file_location, 'r') as schema_file:
        schema_json = json.load(schema_file)
    return schema_json

def validate_data(schema_name: str, request_data: dict) -> None:
    schema = get_schema(schema_name)
    jsonschema.validate(request_data, schema)
