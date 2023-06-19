from typing import Optional, List, TypedDict
from datetime import datetime

from sqlalchemy import func, or_

from quark import db
from quark.models.record import Record, RecordType
from quark.services import account as account_svc


class ListParams(TypedDict):
    record_type: int
    category_id: int
    account_id: int
    year: datetime


def get_list(user_id: int, params: ListParams) -> List[Record]:
    query = db.session.query(Record).\
        filter_by(user_id=user_id, is_deleted=0).\
        filter(Record.record_time >= params['year'].strftime('%Y-01-01 00:00:00')).\
        filter(Record.record_time <= params['year'].strftime('%Y-12-31 23:59:59'))

    if 'record_type' in params:
        query = query.filter_by(record_type=params['record_type'])

    if 'category_id' in params:
        query = query.filter_by(category_id=params['category_id'])

    if 'account_id' in params:
        query = query.filter(or_(
            Record.account_id == params['account_id'],
            Record.target_account_id == params['account_id'],
        ))

    return query.\
        order_by(Record.record_time.desc()).\
        all()


def get_record(user_id: int, record_id: int) -> Optional[Record]:
    return db.session.query(Record).\
        filter_by(user_id=user_id, id=record_id, is_deleted=0).\
        first()


def do_record(record: Record):
    account = account_svc.get_account(record.user_id, record.account_id)
    assert account is not None

    if record.record_type == RecordType.TRANSFER:
        account.balance -= record.amount
        target_account = account_svc.get_account(record.user_id, record.target_account_id)
        assert target_account is not None
        target_account.balance += record.amount

    else:
        account.balance += record.amount


def undo_record(record: Record):
    account = account_svc.get_account(record.user_id, record.account_id)
    assert account is not None

    if record.record_type == RecordType.TRANSFER:
        account.balance += record.amount
        target_account = account_svc.get_account(record.user_id, record.target_account_id)
        assert target_account is not None
        target_account.balance -= record.amount

    else:
        account.balance -= record.amount


def exists_by_account(user_id: int, account_id: int) -> bool:
    row = db.session.query(Record.id).\
        filter_by(user_id=user_id, is_deleted=0).\
        filter(or_(
            Record.account_id == account_id,
            Record.target_account_id == account_id,
        )).\
        first()
    return row is not None


def get_min_date(user_id: int) -> Optional[datetime]:
    return db.session.query(func.min(Record.record_time)).\
        filter_by(user_id=user_id, is_deleted=0).\
        scalar()
