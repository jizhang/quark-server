from flask import Response, jsonify
from flask_login import current_user, login_required

from quark.services import category as category_svc

from . import bp
from .schemas.category import category_schema


@bp.route('/list')
@login_required
def category_list() -> Response:
    rows = category_svc.get_list(current_user.id)
    return jsonify(data=category_schema.dump(rows, many=True))
