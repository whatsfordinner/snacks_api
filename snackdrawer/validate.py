import beeline
import json
import jsonschema
from flask import current_app

@beeline.traced(name='fetching_jsonschema')
def get_schema(schema_name: str) -> dict:
    beeline.add_context_field('schema_name', schema_name)
    schema_file_location = f'snackdrawer/schemas/{schema_name}.json'
    current_app.logger.debug(f'reading in schema file: {schema_file_location}')
    with open(schema_file_location, 'r') as schema_file:
        schema_json = json.load(schema_file)
    return schema_json

@beeline.traced(name='validating_jsonschema')
def validate_data(schema_name: str, request_data: dict) -> None:
    beeline.add_context_field('schema_name', schema_name)
    schema = get_schema(schema_name)
    jsonschema.validate(request_data, schema)
    beeline.add_context_field('result', 'valid_data')
