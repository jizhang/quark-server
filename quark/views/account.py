from flask import Blueprint, Response

from quark import db
from quark.models.account import Account

bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/list')
def account_list() -> Response:
    rows = db.session.query(Account).\
        filter_by(user_id=1).\
        order_by(Account.order_num.asc()).\
        all()

    return str(len(rows))
