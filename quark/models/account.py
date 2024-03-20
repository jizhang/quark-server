from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Account(Base):
    __tablename__ = 'account'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    name: Mapped[str]
    type: Mapped[int]
    initial_balance: Mapped[Decimal]
    balance: Mapped[Decimal]
    order_num: Mapped[int]
    is_hidden: Mapped[int]
    is_deleted: Mapped[int]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]


class AccountType:
    ASSET = 1
    LIABILITY = 2

    @classmethod
    def all(cls):
        return [cls.ASSET, cls.LIABILITY]
