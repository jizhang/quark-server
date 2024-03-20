from datetime import datetime
from decimal import Decimal
from typing import Dict

from dateutil.relativedelta import relativedelta
from sqlalchemy import text

from quark import db
from quark.models.record import RecordType


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
        """,
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
        """,
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
