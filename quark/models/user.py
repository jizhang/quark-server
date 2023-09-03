from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin

from . import Base


class User(Base, UserMixin):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
