from typing import Dict, List, Optional

from quark import db
from quark.models.category import Category
from quark.models.record import RecordType


def get_list(user_id: int) -> List[Category]:
    return db.session.query(Category).\
        filter_by(user_id=user_id, is_deleted=0).\
        order_by(Category.type, Category.name).\
        all()


def get_name_mapping(user_id: int) -> Dict[int, str]:
    rows = db.session.query(Category.id, Category.name).\
        filter_by(user_id=user_id, is_deleted=0).\
        all()

    result: Dict[int, str] = {}
    for row in rows:
        result[row.id] = row.name
    return result


def find_investment_category(user_id: int) -> Optional[Category]:
    return db.session.query(Category).\
        filter_by(user_id=user_id, is_deleted=0).\
        filter_by(type=RecordType.INCOME, name='Investment').\
        first()
