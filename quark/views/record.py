from typing import List
from decimal import Decimal
from datetime import datetime

from flask import Blueprint, Response, jsonify, request
from flask_login import login_required, current_user
from marshmallow import ValidationError

from quark import db, AppError
from quark.models.account import Account
from quark.models.record import Record, RecordType
from quark.services import account as account_svc
from quark.services import category as category_svc
from quark.services import record as record_svc
from quark.utils import row_to_dict, rows_to_list
from .record_item import record_item_schema
from .record_form import record_form_schema

bp = Blueprint('record', __name__, url_prefix='/api/record')


@bp.route('/list')
@login_required
def record_list() -> Response:
    records = record_svc.get_list(current_user.id)
    account_names = account_svc.get_name_mapping(current_user.id)
    category_names = category_svc.get_name_mapping(current_user.id)

    data: List[dict] = []
    for row in records:
        data.append({
            'id': row.id,
            'record_type': row.record_type,
            'category_name': category_names.get(row.category_id),
            'account_name': account_names.get(row.account_id),
            'target_account_name': account_names.get(row.target_account_id),
            'record_time': row.record_time,
            'amount': row.amount,
            'remark': row.remark,
        })

    return jsonify(data=record_item_schema.dump(data, many=True))


@bp.route('/get')
@login_required
def record_get() -> Response:
    raise AppError('Record not found')


@bp.route('/save', methods=['POST'])
@login_required
def record_save() -> Response:
    try:
        form = record_form_schema.load(request.json)
    except ValidationError as e:
        raise AppError(str(e.messages))

    if 'id' in form:
        record = record_svc.get_record(current_user.id, form['id'])
        assert record is not None  # Validated in form.

    else:
        record = Record()
        record.user_id = current_user.id
        record.is_deleted = 0
        record.created_at = datetime.now()

    record.record_type = form['record_type']
    if record.record_type in [RecordType.EXPENSE, RecordType.INCOME]:
        record.category_id = form['category_id']
        record.target_account_id = 0
    elif record.record_type == RecordType.TRANSFER:
        record.category_id = 0
        record.target_account_id = form['target_account_id']
    else:
        assert False

    record.account_id = form['account_id']
    record.record_time = form['record_time']
    record.amount = form['amount']
    record.remark = form['remark']

    if not record.id:
        db.session.add(record)

    db.session.flush()
    record_id = record.id
    db.session.commit()
    return jsonify(id=record_id)
