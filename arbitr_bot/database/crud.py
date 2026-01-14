from sqlalchemy.orm import Session
from ..database.db import Announcement, SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_announcement(db: Session, title: str, content: str, category: str, source_channel: str, source_url: str = None):
    db_announcement = Announcement(
        title=title,
        content=content,
        category=category,
        source_channel=source_channel,
        source_url=source_url
    )
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

def get_announcements_by_category(db: Session, category: str, skip: int = 0, limit: int = 100):
    return db.query(Announcement).filter(Announcement.category == category).offset(skip).limit(limit).all()

def get_announcements_by_keyword(db: Session, keyword: str, skip: int = 0, limit: int = 100):
    return db.query(Announcement).filter(Announcement.content.contains(keyword)).offset(skip).limit(limit).all()

def get_all_categories(db: Session):
    categories = db.query(Announcement.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]