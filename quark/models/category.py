from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    type: Mapped[int]
    name: Mapped[str]
    is_deleted: Mapped[int]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
