from typing import Any, Tuple, List, Dict, TypedDict
from decimal import Decimal
from datetime import datetime

from sqlalchemy import text
from dateutil.relativedelta import relativedelta

from quark import db
from quark.models.record import RecordType
from quark.services import category as category_svc
from . import get_time_range


class TrendRow:
    def __init__(self, month: str, category_id: int, category_name: str, amount: Decimal):
        self.month = month
        self.category_id = category_id
        self.category_name = category_name
        self.amount = amount


class TrendResult(TypedDict):
    categories: List[Dict[str, Any]]
    data: List[Dict[str, Any]]


def get_expense_chart(user_id: int, record_type: int,
                      start_date: datetime, end_date: datetime) -> TrendResult:
    params = {
        'user_id': user_id,
        'record_type': record_type,
        'amount_sign': -1 if record_type == RecordType.EXPENSE else 1,
    }
    params.update(get_time_range(start_date, end_date))

    rows: List[TrendRow] = db.session.execute(text(
        """
        SELECT
            DATE_FORMAT(a.record_time, '%Y%m') AS `month`
            ,a.category_id
            ,MAX(b.name) AS category_name
            ,SUM(a.amount) * :amount_sign AS `amount`
        FROM record a
        JOIN category b ON a.category_id = b.id
        WHERE a.user_id = :user_id
        AND a.is_deleted = 0
        AND a.record_time BETWEEN :start_time AND :end_time
        AND a.record_type = :record_type
        GROUP BY `month`, a.category_id
        """
    ), params).fetchall()

    return make_monthly_trend(rows, start_date, end_date)


def get_investment_trend(user_id: int, start_date: datetime, end_date: datetime) -> TrendResult:
    category = category_svc.find_investment_category(user_id)
    if category is None:
        return make_monthly_trend([], start_date, end_date)

    params = {
        'user_id': user_id,
        'category_id': category.id,
    }
    params.update(get_time_range(start_date, end_date))

    rows: List[TrendRow] = db.session.execute(text(
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


def make_monthly_trend(rows: List[TrendRow], start_date: datetime, end_date: datetime,
                       top_n=5) -> TrendResult:
    category_map: Dict[int, dict] = {}
    month_category_map: Dict[Tuple[str, int], Decimal] = {}
    for row in rows:
        category = category_map.setdefault(row.category_id, {
            'id': row.category_id,
            'name': row.category_name,
            'amount': Decimal(0),
        })
        category['amount'] += row.amount

        month_category_map[(row.month, row.category_id)] = row.amount

    sorted_categories = sorted(category_map.values(), key=lambda x: abs(x['amount']), reverse=True)
    top_categories = sorted_categories[:top_n]
    other_categories = sorted_categories[top_n:]

    data = []
    current_date = start_date
    while current_date < end_date:
        month = current_date.strftime('%Y%m')
        item: dict = {
            'month': month,
        }

        for category in top_categories:
            item[f'category_{category["id"]}'] = \
                month_category_map.get((month, category['id']), Decimal(0))

        if other_categories:
            item['category_0'] = Decimal(0)
            for category in other_categories:
                item['category_0'] += \
                    month_category_map.get((month, category['id']), Decimal(0))

        data.append(item)
        current_date += relativedelta(months=1)

    if other_categories:
        top_categories.append({
            'id': 0,
            'name': 'Other',
        })

    return {
        'categories': top_categories,
        'data': data,
    }
