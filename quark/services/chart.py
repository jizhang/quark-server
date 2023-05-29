from decimal import Decimal
from datetime import datetime

from sqlalchemy import text

from quark import db
from quark.models.record import RecordType
from quark.services import category as category_svc


def get_category_chart(user_id: int, start_date: datetime, end_date: datetime) -> list:
    params = {
        'user_id': user_id,
    }
    params.update(get_time_range(start_date, end_date))

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
        AND a.record_time BETWEEN :start_time AND :end_time
        AND a.is_deleted = 0
        GROUP BY a.record_type, a.category_id
        """
    ), params).fetchall()

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


def get_investment_chart(user_id: int, start_date: datetime, end_date: datetime) -> dict:
    category = category_svc.find_investment_category(user_id)
    if category is None:
        return {
            'record_type': RecordType.INCOME,
            'category_id': 0,
            'total': Decimal(0),
            'accounts': [],
        }

    params = {
        'user_id': user_id,
        'category_id': category.id,
    }
    params.update(get_time_range(start_date, end_date))

    rows = db.session.execute(text(
        """
        SELECT
            a.account_id
            ,b.name AS account_name
            ,SUM(a.amount) AS amount
        FROM record a
        JOIN account b ON a.account_id = b.id
        WHERE a.user_id = :user_id
        AND a.record_time BETWEEN :start_time AND :end_time
        AND a.category_id = :category_id
        AND a.is_deleted = 0
        GROUP BY a.account_id
        """
    ), params).fetchall()

    total = Decimal(0)
    positive_total = Decimal(0)
    accounts = []
    for row in rows:
        total += row.amount
        if row.amount > 0:
            positive_total += row.amount

        accounts.append({
            'id': row.account_id,
            'name': row.account_name,
            'amount': row.amount,
            'percent': 0.0,
        })

    if positive_total > 0:
        for item in accounts:
            if item['amount'] > 0:
                item['percent'] = item['amount'] / positive_total

    accounts.sort(key=lambda x: x['amount'], reverse=True)

    return {
        'record_type': category.type,
        'category_id': category.id,
        'total': total,
        'accounts': accounts,
    }


def get_time_range(start_date: datetime, end_date: datetime):
    return {
        'start_time': start_date.strftime('%Y-%m-%d 00:00:00'),
        'end_time': end_date.strftime('%Y-%m-%d 23:59:59'),
    }
