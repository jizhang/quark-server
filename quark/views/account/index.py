from datetime import datetime

from flask import Response, jsonify, request
from flask_login import current_user, login_required

from quark import AppError, db
from quark.models.account import Account
from quark.services import account as account_svc
from quark.services import record as record_svc

from . import bp
from .schemas.account import account_schema
from .schemas.account_move import account_move_schema
from .schemas.account_request import account_request_schema


@bp.route('/list')
@login_required
def account_list() -> Response:
    rows = account_svc.get_account_list(current_user.id)
    return jsonify(data=account_schema.dump(rows, many=True))


@bp.route('/get')
@login_required
def account_get() -> Response:
    account = account_request_schema.load(request.args)
    return jsonify(account=account_schema.dump(account))


@bp.route('/save', methods=['POST'])
@login_required
def account_save() -> Response:
    form = account_schema.load(request.get_json())

    if 'id' in form:  # Editing
        account = account_svc.get_account(current_user.id, form['id'])
        assert account is not None  # Validated in schema.
    else:
        account = Account()

    account.name = form['name']
    account.is_hidden = form['is_hidden']

    if account.id is None:  # Adding
        account.user_id = current_user.id
        account.type = form['type']
        account.initial_balance = form['initial_balance']
        account.balance = account.initial_balance
        account.order_num = account_svc.get_max_order_num(current_user.id) + 10
        account.is_deleted = 0
        account.created_at = datetime.now()

        db.session.add(account)
        db.session.flush()

    account_id = account.id
    db.session.commit()
    return jsonify(id=account_id)


@bp.route('/delete', methods=['POST'])
@login_required
def account_delete() -> Response:
    account = account_request_schema.load(request.get_json())

    if record_svc.exists_by_account(current_user.id, account.id):
        raise AppError('Account still has records.')

    account.is_deleted = 1
    account_id = account.id
    db.session.commit()
    return jsonify(id=account_id)


@bp.post('/move')
@login_required
def account_move() -> Response:
    form = account_move_schema.load(request.json)  # type: ignore
    account_svc.move_account(current_user.id, form['active_id'], form['over_id'])
    db.session.commit()
    return jsonify('ok')
