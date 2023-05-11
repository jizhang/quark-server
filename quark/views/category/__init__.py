from flask import Blueprint, Response, jsonify
from flask_login import current_user

from quark.services import category as category_svc
from .category_schema import category_schema

bp = Blueprint('category', __name__, url_prefix='/api/category')


@bp.route('/list')
def category_list() -> Response:
    rows = category_svc.get_list(current_user.id)
    return jsonify(data=category_schema.dump(rows, many=True))
