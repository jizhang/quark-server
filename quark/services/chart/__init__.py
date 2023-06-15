from typing import Tuple, Dict
from decimal import Decimal
from datetime import datetime

from sqlalchemy import text
from dateutil.relativedelta import relativedelta

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

    group_map: Dict[int, dict] = {
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


def get_net_capital_chart(user_id: int, start_date: datetime, end_date: datetime) -> list:
    params = {
        'user_id': user_id,
        'record_types': [RecordType.EXPENSE, RecordType.INCOME],
    }

    account_rows = db.session.execute(text(
        """
        SELECT
            DATE_FORMAT(created_at, '%Y%m') AS `month`
            ,SUM(initial_balance) AS initial_balance
        FROM account
        WHERE user_id = :user_id
        AND is_deleted = 0
        GROUP BY `month`
        """
    ), params).fetchall()

    record_rows = db.session.execute(text(
        """
        SELECT
            DATE_FORMAT(record_time, '%Y%m') AS `month`
            ,SUM(amount) AS amount
        FROM record
        WHERE user_id = :user_id
        AND record_type IN :record_types
        AND is_deleted = 0
        GROUP BY `month`
        """
    ), params).fetchall()

    amount_map: Dict[str, Decimal] = {row.month: row.initial_balance for row in account_rows}
    for row in record_rows:
        amount_map.setdefault(row.month, Decimal(0))
        amount_map[row.month] += row.amount

    start_month = start_date.strftime('%Y%m')
    min_month = start_month
    if amount_map:
        min_month = min(min_month, min(amount_map.keys()))

    clock_month = datetime.now().strftime('%Y%m')
    result = []
    net_capital = Decimal(0)
    current_date = datetime.strptime(min_month, '%Y%m')
    while current_date < end_date:
        current_month = current_date.strftime('%Y%m')
        net_capital += amount_map.get(current_month, Decimal(0))
        if current_month >= start_month:
            result.append({
                'month': current_month,
                'amount': net_capital if current_month <= clock_month else None,
            })

        current_date += relativedelta(months=1)

    return result


def get_expense_chart(user_id: int, record_type: int,
                      start_date: datetime, end_date: datetime) -> dict:
    params = {
        'user_id': user_id,
        'record_type': record_type,
        'amount_sign': -1 if record_type == RecordType.EXPENSE else 1,
    }
    params.update(get_time_range(start_date, end_date))

    rows = db.session.execute(text(
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


def make_monthly_trend(rows: list, start_date: datetime, end_date: datetime) -> dict:
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

    sorted_categories = sorted(category_map.values(), key=lambda x: x['amount'], reverse=True)
    top_n = 5
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


def get_time_range(start_date: datetime, end_date: datetime):
    return {
        'start_time': start_date.strftime('%Y-%m-%d 00:00:00'),
        'end_time': end_date.strftime('%Y-%m-%d 23:59:59'),
    }
