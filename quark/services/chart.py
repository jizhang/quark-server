from decimal import Decimal
from datetime import datetime

from sqlalchemy import text

from quark import db
from quark.models.record import RecordType


def get_category_chart(user_id: int, start_date: datetime, end_date: datetime) -> list:
    rows = db.session.execute(text(
        """
        SELECT
            a.record_type
            ,a.category_id
            ,b.name AS category_name
            ,SUM(a.amount) AS amount
        FROM record a
        JOIN category b ON a.category_id = b.id
        WHERE a.user_id = :user_id
        AND a.record_time BETWEEN :start_date AND :end_date
        GROUP BY a.record_type, a.category_id
        """
    ), {
        'user_id': user_id,
        'start_date': start_date,
        'end_date': end_date,
    }).fetchall()

    group_map = {
        RecordType.EXPENSE: {
            'id': RecordType.EXPENSE,
            'name': 'Expense',
            'amount': Decimal(0),
            '_total_amount': Decimal(0),
            'categories': [],
        },
        RecordType.INCOME: {
            'id': RecordType.INCOME,
            'name': 'Income',
            'amount': Decimal(0),
            '_total_amount': Decimal(0),
            'categories': [],
        }
    }
    for row in rows:
        group = group_map.get(row.record_type)
        if group is None:
            continue

        if row.record_type == RecordType.EXPENSE and row.amount != 0:
            group['amount'] += -row.amount
            amount = -row.amount

        else:
            group['amount'] += row.amount
            amount = row.amount

        if amount > 0:
            group['_total_amount'] += amount

        group['categories'].append({
            'id': row.category_id,
            'name': row.category_name,
            'amount': amount,
            'percent': 0.0,
        })

    for group in group_map.values():
        if group['_total_amount'] > 0:
            for item in group['categories']:
                if item['amount'] > 0:
                    item['percent'] = item['amount'] / group['_total_amount']
        group['categories'].sort(key=lambda x: x['amount'], reverse=True)

    return list(group_map.values())
