from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from datetime import datetime
from .base import Base
from . import TariffType

class AccessKey(Base):
    __tablename__ = "access_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)  # Статус ключа (активен/использован)
    tariff = Column(Enum(TariffType), nullable=False)  # Привязка к тарифу
    created_at = Column(DateTime, default=datetime.utcnow)
