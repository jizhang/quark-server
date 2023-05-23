from datetime import datetime

from flask import request, Response, jsonify
from flask_login import login_required, current_user
from marshmallow import ValidationError
from dateutil.relativedelta import relativedelta

from quark import AppError
from quark.services import record as record_svc, chart as chart_svc
from . import bp
from .schemas.category_chart_request import category_chart_request_schema
from .schemas.category_chart_response import category_chart_response_schema


@bp.get('/min-date')
@login_required
def chart_min_date() -> Response:
    dt = record_svc.get_min_date(current_user.id)
    if dt is None:
        dt = datetime.now()
    return jsonify(min_date=int(dt.strftime('%Y%m%d')))


@bp.get('/category')
@login_required
def chart_category() -> Response:
    try:
        form = category_chart_request_schema.load(request.args)
    except ValidationError as e:
        raise AppError(str(e.messages))

    start_date = form['month']
    end_date = start_date + relativedelta(day=31)
    data = chart_svc.get_category_chart(current_user.id, form['type'], start_date, end_date)

    return category_chart_response_schema.dump({'data': data})
