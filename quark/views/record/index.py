from flask import Response, jsonify, request
from flask_login import current_user, login_required

from quark.services import account as account_svc
from quark.services import category as category_svc
from quark.services import record as record_svc

from . import bp
from .schemas.record_item import RecordItemSchema
from .schemas.record_list_request import record_list_request_schema


@bp.get('/list')
@login_required
def record_list() -> Response:
    form = record_list_request_schema.load(request.args)
    records = record_svc.get_list(current_user.id, form)

    schema = RecordItemSchema()
    schema.context = {
        'category_names': category_svc.get_name_mapping(current_user.id),
        'account_names': account_svc.get_name_mapping(current_user.id),
    }

    return jsonify(data=schema.dump(records, many=True))
