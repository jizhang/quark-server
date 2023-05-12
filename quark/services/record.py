from typing import Optional, List

from quark import db
from quark.models.record import Record, RecordType
from quark.services import account as account_svc


def get_list(user_id: int, last_id=0, limit=100_000, account_id: Optional[int] = None) -> List[Record]:
    query = db.session.query(Record).\
        filter_by(user_id=user_id, is_deleted=0).\
        filter(Record.id > last_id)

    if account_id is not None:
        query = query.filter_by(account_id=account_id)

    return query.\
        order_by(Record.record_time.desc()).\
        limit(limit).\
        all()


def get_record(user_id: int, record_id: int) -> Optional[Record]:
    return db.session.query(Record).\
        filter_by(user_id=user_id, id=record_id, is_deleted=0).\
        first()


def do_record(record: Record):
    account = account_svc.get_account(record.user_id, record.account_id)
    assert account is not None
    account.balance += record.amount

    if record.record_type == RecordType.TRANSFER:
        target_account = account_svc.get_account(record.user_id, record.target_account_id)
        assert target_account is not None
        target_account.balance -= record.amount


def undo_record(record: Record):
    account = account_svc.get_account(record.user_id, record.account_id)
    assert account is not None
    account.balance -= record.amount

    if record.record_type == RecordType.TRANSFER:
        target_account = account_svc.get_account(record.user_id, record.target_account_id)
        assert target_account is not None
        target_account.balance += record.amount


def exists_by_account(user_id: int, account_id: int) -> bool:
    row = db.session.query(Record.id).\
        filter_by(user_id=user_id, account_id=account_id, is_deleted=0).\
        first()
    return row is not None
