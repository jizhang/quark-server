from typing import Optional, List

from quark import db
from quark.models.record import Record


def get_list(user_id: int, last_id=0, limit=100, account_id: Optional[int] = None) -> List[Record]:
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
