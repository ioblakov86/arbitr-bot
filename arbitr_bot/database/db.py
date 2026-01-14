from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///arbitr_bot.db')
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    category = Column(String, index=True)
    source_channel = Column(String, index=True)
    source_url = Column(String)
    published_date = Column(DateTime, default=datetime.utcnow)
    parsed_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

# Create tables
Base.metadata.create_all(bind=engine)