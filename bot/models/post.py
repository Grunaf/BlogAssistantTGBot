from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, nullable=False)  # Уникальный идентификатор сообщения в рамках канала
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)  # Внешний ключ
    text = Column(String, nullable=False)
    has_image = Column(Boolean, default=False)  # Флаг наличия изображения
    has_video = Column(Boolean, default=False)  # Флаг наличия видео
    published_at = Column(DateTime, default=datetime.utcnow)

    channel = relationship("Channel", back_populates="posts")
    user = relationship("User", back_populates="posts")
    metrics = relationship("PostMetric", back_populates="post")

class PostMetric(Base):
    __tablename__ = 'post_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    collected_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="metrics")
