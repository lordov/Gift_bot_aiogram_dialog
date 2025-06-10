from sqlalchemy import (
    Integer, String, Boolean, 
    DateTime, ForeignKey, Text, UniqueConstraint
)

from sqlalchemy.orm import (
    relationship, mapped_column, Mapped
)

from tgbot.database.engine import Base
from datetime import datetime



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=False)

    participations = relationship("Participation", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, chat_id={self.chat_id})>"


class Participation(Base):
    __tablename__ = "participations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    participation_number: Mapped[str] = mapped_column(String(255))
    participation_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now)
    month: Mapped[int] = mapped_column(Integer)
    year: Mapped[int] = mapped_column(Integer)
    screenshot_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="participations")
    
    # Добавляем уникальный ключ для ограничения участия (один раз в месяц)
    __table_args__ = (
        UniqueConstraint('user_id', 'month', 'year', name='uq_participation_once_per_month'),
    )


class GiveawaySettings(Base):
    __tablename__ = "giveaway_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(Integer)
    year: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    image_path: Mapped[str] = mapped_column(String(255), nullable=True)
    channel_id: Mapped[str] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
