from typing import Dict
from datetime import datetime

from quark import db
from sqlalchemy import text

from quark.services import category as category_svc
from . import get_time_range, make_monthly_trend


def get_investment_trend(user_id: int, start_date: datetime, end_date: datetime) -> dict:
    result: Dict[str, list] = {
        'categories': [],
        'data': [],
    }

    category = category_svc.find_investment_category(user_id)
    if category is None:
        return result

    params = {
        'user_id': user_id,
        'category_id': category.id,
    }
    params.update(get_time_range(start_date, end_date))

    rows = db.session.execute(text(
        """
        SELECT
            DATE_FORMAT(a.record_time, '%Y%m') AS `month`
            ,a.account_id AS category_id
            ,MAX(b.name) AS category_name
            ,SUM(a.amount) AS amount
        FROM record a
        JOIN account b ON a.account_id = b.id
        WHERE a.user_id = :user_id
        AND a.is_deleted = 0
        AND a.category_id = :category_id
        AND a.record_time BETWEEN :start_time AND :end_time
        GROUP BY `month`, a.account_id
        """
    ), params).fetchall()

    return make_monthly_trend(rows, start_date, end_date)
