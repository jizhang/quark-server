from typing import Optional, List, Dict

from sqlalchemy import select

from quark import db
from quark.models.account import Account


def get_account_list(user_id: int) -> List[Account]:
    return db.session.query(Account).\
        filter_by(user_id=user_id, is_deleted=0).\
        order_by(Account.order_num.asc()).\
        all()


def get_name_mapping(user_id: int) -> Dict[int, str]:
    rows = db.session.query(Account.id, Account.name).\
        filter_by(user_id=user_id, is_deleted=0).\
        all()

    result: Dict[int, str] = {}
    for row in rows:
        result[row.id] = row.name
    return result


def get_account(user_id: int, account_id: int) -> Optional[Account]:
    return db.session.query(Account).\
        filter_by(user_id=user_id, id=account_id, is_deleted=0).\
        first()


def get_account_by_name(user_id: int, name: str) -> Optional[Account]:
    return db.session.query(Account).\
        filter_by(user_id=user_id, name=name, is_deleted=0).\
        first()


def get_max_order_num(user_id: int) -> int:
    row = db.session.query(Account.order_num).\
        filter_by(user_id=user_id, is_deleted=0).\
        order_by(Account.order_num.desc()).\
        first()
    return 0 if row is None else row.order_num


def move_account(user_id: int, active_id: int, over_id: int):
    accounts = db.session.scalars(
        select(Account)
        .filter_by(user_id=user_id, is_deleted=0)
        .order_by(Account.order_num)
    ).all()

    reordered_accounts: List[Account] = []
    active_account = None
    over_index = None
    for i, account in enumerate(accounts):
        if active_account is None and account.id == active_id:
            active_account = account
            continue

        if over_index is None and account.id == over_id:
            over_index = i

        reordered_accounts.append(account)

    if active_account is None or over_index is None:
        return  # This should never happen.

    reordered_accounts.insert(over_index, active_account)

    order_num = 10
    for account in reordered_accounts:
        account.order_num = order_num
        order_num += 10
