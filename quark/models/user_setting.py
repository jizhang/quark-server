from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class UserSetting(Base):
    __tablename__ = 'user_setting'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    setting_key: Mapped[str]
    setting_value_json: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
