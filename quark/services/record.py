from typing import Optional

from quark import db
from quark.models.record import Record


def get_record(user_id: int, record_id: int) -> Optional[Record]:
    return db.session.query(Record).\
        filter_by(user_id=user_id, id=record_id, is_deleted=0).\
        first()
