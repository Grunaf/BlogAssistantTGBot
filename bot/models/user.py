from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float, DateTime, Boolean, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
import enum


class TariffType(enum.Enum):
    Basic = "basic"
    Advanced = "advanced"
    Premium = "premium"

class UserRole(enum.Enum):
    Blogger = "blogger"
    Audience = "audience"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    chat_id = Column(BigInteger, nullable=True)  # Поле для сохранения chat_id
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    role = Column(Enum(UserRole), nullable=False)  # Новое поле для роли
    is_confirmed_blogger = Column(Boolean, default=False)  # Статус подтверждения
    loyalty_points = Column(Float, default=0)
    tariff = Column(Enum(TariffType), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bot_metrics = relationship("BotMetric", back_populates="user")
    posts = relationship("Post", back_populates="user")
    tariff_history = relationship("TariffHistory", back_populates="user")
    channels = relationship("Channel", back_populates="user")  # Связь с каналами

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=True)
    username = Column(String, nullable=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="channels")
    posts = relationship("Post", back_populates="channel")  # Связь с постами

class TariffHistory(Base):
    __tablename__ = 'tariff_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    old_tariff = Column(Enum(TariffType), nullable=False)
    new_tariff = Column(Enum(TariffType), nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tariff_history")
