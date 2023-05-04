from decimal import Decimal
from datetime import datetime

from flask import Blueprint, Response, jsonify, request
from flask_login import login_required, current_user

from quark import db, AppError
from quark.models.account import Account
from quark.services import account as account_svc
from quark.utils import row_to_dict, rows_to_list

bp = Blueprint('account', __name__, url_prefix='/api/account')


@bp.route('/list')
@login_required
def account_list() -> Response:
    rows = account_svc.get_account_list(current_user.id)
    return jsonify(data=rows_to_list(rows))


@bp.route('/get')
@login_required
def account_get() -> Response:
    account = check_account_id(current_user.id, request.args.get('id'))
    return jsonify(account=row_to_dict(account))


@bp.route('/save', methods=['POST'])
@login_required
def account_save() -> Response:
    form = request.get_json()
    user_id = current_user.id

    if not isinstance(form, dict):
        raise AppError('Invalid request body')

    if form.get('id'):  # Editing
        account = check_account_id(user_id, form['id'])
    else:
        account = Account()

    if not form.get('name'):
        raise AppError('Account name cannot be empty.')

    # Check name collision
    by_name = account_svc.get_account_by_name(user_id, form['name'])
    if by_name is not None and (account.id is None or by_name.id != account.id):
        raise AppError('Account name is duplicate.')

    account.name = form['name']

    if account.id is None:  # Adding
        account.user_id = user_id
        account.type = check_account_type(form)
        account.initial_balance = check_initial_balance(form)
        account.balance = account.initial_balance
        account.order_num = account_svc.get_max_order_num(user_id) + 10
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
    account = check_account_id(current_user.id, request.json.get('id'))

    # TODO Check records.

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


def check_account_type(form: dict) -> int:
    if not form.get('type'):
        raise AppError('Account type cannot be empty.')

    try:
        account_type = int(form['type'])
        if account_type not in (1, 2):
            raise ValueError

    except ValueError:
        raise AppError('Invalid account type')

    else:
        return account_type


def check_initial_balance(form: dict) -> Decimal:
    if not form.get('initial_balance'):
        return Decimal(0)

    try:
        return Decimal(form['initial_balance'])
    except Exception:
        raise AppError('Invalid initial balance')
