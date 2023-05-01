from typing import List

from quark import db
from quark.models.account import Account


def get_account_list(user_id: int) -> List[Account]:
    return db.session.query(Account).\
        filter_by(user_id=user_id).\
        order_by(Account.order_num.asc()).\
        all()
