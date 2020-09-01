import jsonschema
from flask import abort, Blueprint, current_app, jsonify, make_response, request
from snackdrawer import db
from snackdrawer.users import jwt_required
from snackdrawer.validate import validate_data

def find_by_name(user_claims: dict, name: str) -> object:
    pass

def find_by_id(user_claims: dict, id: int) -> object:
    pass

def get_user_drawers(user_claims: dict) -> list:
    pass

def get_contents(drawer_id: int) -> list:
    snacks = []
    results = db.get_db().get_snacks_in_drawer(drawer_id)
    for result in results:
            snacks.append(result)
    
    return snacks