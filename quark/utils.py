from typing import Iterable, List
from decimal import Decimal
from datetime import datetime

from sqlalchemy import Row
from sqlalchemy.orm import DeclarativeMeta


def row_to_dict(row) -> dict:
    if isinstance(row, Row):
        row_dict = dict(row)
    elif isinstance(row.__class__, DeclarativeMeta):
        row_dict = {c.name: getattr(row, c.name) for c in row.__table__.columns}
    else:
        raise ValueError('Unsupported row type.')

    for key, value in row_dict.items():
        if isinstance(value, Decimal):
            row_dict[key] = float(value)
        elif isinstance(value, datetime):
            row_dict[key] = value.strftime('%Y-%m-%d %H:%M:%S')

    return row_dict


def rows_to_list(rows: Iterable) -> List[dict]:
    return [row_to_dict(i) for i in rows]
