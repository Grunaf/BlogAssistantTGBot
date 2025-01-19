from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.models.base import Base
from bot.models import *

from bot.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
