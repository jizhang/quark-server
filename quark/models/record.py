from decimal import Decimal
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Record(Base):
    __tablename__ = 'record'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    record_type: Mapped[int]
    category_id: Mapped[int]
    account_id: Mapped[int]
    target_account_id: Mapped[int]
    record_time: Mapped[datetime]
    amount: Mapped[Decimal]
    remark: Mapped[str]
    is_deleted: Mapped[int]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]


class RecordType:
    EXPENSE = 1
    INCOME = 2
    TRANSFER = 3

    @classmethod
    def all(cls):
        return [cls.EXPENSE, cls.INCOME, cls.TRANSFER]
