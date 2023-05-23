from decimal import Decimal
from datetime import datetime

from sqlalchemy import text

from quark import db
from quark.models.record import RecordType


def get_category_chart(user_id: int, record_type: int, start_date: datetime, end_date: datetime) -> list:
    rows = db.session.execute(text(
        """
        SELECT
            a.category_id
            ,b.name AS category_name
            ,SUM(a.amount) AS amount
        FROM record a
        JOIN category b ON a.category_id = b.id
        WHERE a.user_id = :user_id
        AND a.record_type = :record_type
        AND a.record_time BETWEEN :start_date AND :end_date
        GROUP BY a.category_id
        """
    ), {
        'user_id': user_id,
        'record_type': record_type,
        'start_date': start_date,
        'end_date': end_date,
    }).fetchall()

    data = []
    total_amount = Decimal(0)
    for row in rows:
        if record_type == RecordType.EXPENSE and row.amount != 0:
            amount = -row.amount
        else:
            amount = row.amount

        if amount > 0:
            total_amount += amount

        data.append({
            'category_id': row.category_id,
            'category_name': row.category_name,
            'amount': amount,
            'percent': 0.0,
        })

    if total_amount > 0:
        for item in data:
            if item['amount'] > 0:
                item['percent'] = item['amount'] / total_amount

    data.sort(key=lambda x: x['amount'], reverse=True)
    return data
