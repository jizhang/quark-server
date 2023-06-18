from datetime import datetime

from flask import Response, jsonify, request
from flask_login import login_required, current_user
from marshmallow import ValidationError

from quark import db, AppError
from quark.models.account import Account
from quark.services import account as account_svc
from quark.services import record as record_svc

from . import bp
from .schemas.account import account_schema


@bp.route('/list')
@login_required
def account_list() -> Response:
    rows = account_svc.get_account_list(current_user.id)
    return jsonify(data=account_schema.dump(rows, many=True))


@bp.route('/get')
@login_required
def account_get() -> Response:
    account = check_account_id(current_user.id, request.args.get('id'))
    return jsonify(account=account_schema.dump(account))


@bp.route('/save', methods=['POST'])
@login_required
def account_save() -> Response:
    try:
        form = account_schema.load(request.json)  # type: ignore
    except ValidationError as e:
        raise AppError(str(e.messages))

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
    if request.json is None:
        raise AppError('Invalid request body')

    account = check_account_id(current_user.id, request.json.get('id'))
    if record_svc.exists_by_account(current_user.id, account.id):
        raise AppError('Account still has records.')

    account.is_deleted = 1
    account_id = account.id
    db.session.commit()
    return jsonify(id=account_id)


def check_account_id(user_id: int, account_id) -> Account:
    try:
        account_id = int(account_id)
    except ValueError:
        raise AppError('Invalid account ID')

    account = account_svc.get_account(user_id, account_id)
    if account is None:
        raise AppError('Account not found')

    return account
