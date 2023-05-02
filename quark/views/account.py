from datetime import datetime

from flask import Blueprint, Response, jsonify, request

from quark import db, AppError
from quark.models.account import Account
from quark.services import account as account_svc
from quark.utils import rows_to_list

bp = Blueprint('account', __name__, url_prefix='/api/account')


@bp.route('/list')
def account_list() -> Response:
    rows = account_svc.get_account_list(1)
    return jsonify(data=rows_to_list(rows))


@bp.route('/save', methods=['POST'])
def account_save() -> Response:
    form = request.get_json()
    user_id = 1

    if 'id' in form:
        try:
            account_id = int(form['id'])
        except ValueError:
            raise AppError('Invalid account ID')

        account = account_svc.get_account(user_id, account_id)
        if account is None:
            raise AppError('Account not found')

        if not form.get('name'):
            raise AppError('Account name cannot be empty.')

        # Check name collision
        by_name = account_svc.get_account_by_name(user_id, form['name'])
        if by_name is not None and by_name.id != account.id:
            raise AppError('Account name is duplicate.')

        account.name = form['name']
        db.session.commit()

        return jsonify(id=account_id)

    else:
        if not form.get('name'):
            raise AppError('Account name cannot be empty.')

        by_name = account_svc.get_account_by_name(user_id, form['name'])
        if by_name is not None:
            raise AppError('Account name is duplicate.')

        if form.get('type') not in ['1', '2']:
            raise AppError('Invalid account type')

        if form.get('initial_balance'):
            try:
                initial_balance = float(form['initial_balance'])
            except ValueError:
                raise AppError('Invalid initial balance')
        else:
            initial_balance = 0

        account = Account()
        account.user_id = user_id
        account.name = form['name']
        account.type = int(form['type'])
        account.initial_balance = initial_balance
        account.balance = initial_balance
        account.order_num = account_svc.get_max_order_num(user_id) + 10
        account.created_at = datetime.now()

        db.session.add(account)
        db.session.flush()
        account_id = account.id
        db.session.commit()

        return jsonify(id=account_id)
