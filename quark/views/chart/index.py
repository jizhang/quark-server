from datetime import datetime

from flask import Response, jsonify, request
from flask_login import current_user, login_required

from quark.models.record import RecordType
from quark.services import record as record_svc
from quark.services.chart import (
    category as category_chart_svc,
)
from quark.services.chart import (
    category_trend as category_trend_chart_svc,
)
from quark.services.chart import (
    net_capital as net_capital_chart_svc,
)

from . import bp
from .schemas import expense_income_chart_response
from .schemas.category_chart_request import category_chart_request_schema
from .schemas.category_chart_response import category_chart_response_schema
from .schemas.investment_chart_response import investment_chart_response_schema
from .schemas.net_capital_chart_request import net_capital_chart_request_schema
from .schemas.net_capital_chart_response import net_capital_chart_response_schema


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
    form = category_chart_request_schema.load(request.args)
    groups = category_chart_svc.get_category_chart(
        current_user.id, form['start_date'], form['end_date'])
    return category_chart_response_schema.dump({'groups': groups})


@bp.get('/investment')
@login_required
def chart_investment() -> Response:
    form = category_chart_request_schema.load(request.args)
    payload = category_chart_svc.get_investment_chart(
        current_user.id, form['start_date'], form['end_date'])
    return investment_chart_response_schema.dump(payload)


@bp.get('/net-capital')
@login_required
def chart_net_capital() -> Response:
    form = net_capital_chart_request_schema.load(request.args)
    data = net_capital_chart_svc.get_net_capital_chart(
        current_user.id, form['start_date'], form['end_date'])
    return net_capital_chart_response_schema.dump({'data': data})


@bp.get('/expense')
@login_required
def chart_expense() -> Response:
    form = net_capital_chart_request_schema.load(request.args)
    payload = category_trend_chart_svc.get_expense_chart(
        current_user.id, RecordType.EXPENSE, form['start_date'], form['end_date'])
    payload_schema = expense_income_chart_response.create_schema(payload['categories'])
    return payload_schema.dump(payload)


@bp.get('/income')
@login_required
def chart_income() -> Response:
    form = net_capital_chart_request_schema.load(request.args)
    payload = category_trend_chart_svc.get_expense_chart(
        current_user.id, RecordType.INCOME, form['start_date'], form['end_date'])
    payload_schema = expense_income_chart_response.create_schema(payload['categories'])
    return payload_schema.dump(payload)


@bp.get('/investment-trend')
@login_required
def chart_investment_trend() -> Response:
    form = net_capital_chart_request_schema.load(request.args)
    payload = category_trend_chart_svc.get_investment_trend(
        current_user.id, form['start_date'], form['end_date'])
    payload_schema = expense_income_chart_response.create_schema(payload['categories'])
    return payload_schema.dump(payload)
