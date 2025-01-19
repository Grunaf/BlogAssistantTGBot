from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
import enum

class Action(enum.Enum):
    DownloadedChecklist = "downloaded_checklist"
    CompletedTest = "completed_test"
    EarnedLoyaltyPoints = "earned_loyalty_points"
    RedeemedLoyaltyPoints = "redeemed_loyalty_points"
    ViewedMaterial = "viewed_material"
    StartedTest = "started_test"

class BotMetric(Base):
    __tablename__ = 'bot_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity_type = Column(Enum(Action), nullable=False)
    activity_name = Column(String, nullable=False)
    result = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bot_metrics")
