from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.models.base import Base
from bot.models import *

import os

engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
