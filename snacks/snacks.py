import logging
from flask import abort, Blueprint, request

logger = logging.getLogger(__name__)
bp = Blueprint('snacks', __name__, '/snacks')

@bp.route('/', methods=['GET'])
def get_snacks() -> dict:
    pass

@bp.route('/<int:snack_id>', methods=['GET'])
def get_snack(snack_id: int) -> dict:
    pass

@bp.route('/', methods=['POST'])
def new_snack() -> dict:
    pass