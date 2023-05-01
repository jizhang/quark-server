from flask import Blueprint, Response, jsonify

from quark.services import account as account_svc
from quark.utils import rows_to_list

bp = Blueprint('account', __name__, url_prefix='/api/account')


@bp.route('/list')
def account_list() -> Response:
    rows = account_svc.get_account_list(1)
    return jsonify(data=rows_to_list(rows))
