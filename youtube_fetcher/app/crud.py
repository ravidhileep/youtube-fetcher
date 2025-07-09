from sqlalchemy.orm import Session
from .models import Video

def get_video_by_id(db: Session, video_id: str):
    return db.query(Video).filter(Video.video_id == video_id).first()

def add_video(db: Session, video: Video):
    db.add(video)
    db.commit()

def get_videos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Video).order_by(Video.published_at.desc()).offset(skip).limit(limit).all()
