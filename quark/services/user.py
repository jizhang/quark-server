import json
from typing import Any, Optional, Union, Dict
from datetime import datetime

from quark import db
from quark.models.user import User
from quark.models.user_setting import UserSetting


def get_user(user_id: Union[int, str]) -> Optional[User]:
    return db.session.query(User).get(user_id)


def get_by_username(username: str) -> Optional[User]:
    return db.session.query(User).\
        filter_by(username=username).\
        first()


def get_user_setting(user_id: int) -> Dict[str, Any]:
    rows = db.session.query(UserSetting).\
        filter_by(user_id=user_id).\
        all()

    return {row.setting_key: json.loads(row.setting_value_json) for row in rows}


def save_user_setting(user_id: int, data: Dict[str, Any]):
    rows = db.session.query(UserSetting).\
        filter_by(user_id=user_id).\
        all()

    row_map = {row.setting_key: row for row in rows}

    for key, value in data.items():
        value_json = json.dumps(value)
        if key in row_map:
            row_map[key].setting_value_json = value_json
        else:
            row = UserSetting()
            row.user_id = user_id
            row.setting_key = key
            row.setting_value_json = value_json
            row.created_at = datetime.now()
            db.session.add(row)
