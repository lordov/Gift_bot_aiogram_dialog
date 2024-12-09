from sqlalchemy import (
   Integer, String, Boolean
)

from sqlalchemy.orm import (
    relationship, mapped_column, Mapped
)

from tgbot.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    participate: Mapped[int] = mapped_column(Integer, default=0)
    number_of_part: Mapped[str] = mapped_column(String(255), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, chat_id={self.chat_id})>"
