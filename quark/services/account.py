from typing import List, Optional

from quark import db
from quark.models.account import Account


def get_account_list(user_id: int) -> List[Account]:
    return db.session.query(Account).\
        filter_by(user_id=user_id).\
        order_by(Account.order_num.asc()).\
        all()


def get_account(user_id: int, account_id: int) -> Optional[Account]:
    return db.session.query(Account).\
        filter_by(user_id=user_id, id=account_id).\
        first()


def get_account_by_name(user_id: int, name: str) -> Optional[Account]:
    return db.session.query(Account).\
        filter_by(user_id=user_id, name=name).\
        first()


def get_max_order_num(user_id: int) -> int:
    row = db.session.query(Account.order_num).\
        filter_by(user_id=user_id).\
        order_by(Account.order_num.desc()).\
        first()
    return 0 if row is None else row.order_num
