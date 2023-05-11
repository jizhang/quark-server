from datetime import datetime

from flask import Response, jsonify, request
from flask_login import login_required, current_user
from marshmallow import ValidationError

from quark import db, AppError
from quark.models.record import Record, RecordType
from quark.services import record as record_svc
from . import bp
from .schemas.record_form import record_form_schema
from .schemas.record_request import record_request_schema


@bp.route('/get')
@login_required
def record_get() -> Response:
    try:
        row = record_request_schema.load(request.args)
    except ValidationError as e:
        raise AppError(str(e.messages))

    return jsonify(record_form_schema.dump(row))


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
