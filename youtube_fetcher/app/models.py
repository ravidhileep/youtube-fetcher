from sqlalchemy import Column, String, DateTime, Integer, Text
from .database import Base

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String(32), unique=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    published_at = Column(DateTime, index=True)
    thumbnail_url = Column(String(255))
    channel_title = Column(String(255))
