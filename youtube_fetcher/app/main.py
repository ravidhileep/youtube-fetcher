from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from .database import SessionLocal, engine, Base
from .models import Video
from .youtube import YouTubeFetcher
import asyncio

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/videos")
def list_videos(
    page: int = Query(1, gt=0),
    size: int = Query(10, le=50),
    search: str = Query(None),
    channel: str = Query(None),
    sort: str = Query("published_at"),
    order: str = Query("desc"),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * size
    query = db.query(Video)
    if search:
        query = query.filter(Video.title.ilike(f"%{search}%"))
    if channel:
        query = query.filter(Video.channel_title.ilike(f"%{channel}%"))
    sort_column = getattr(Video, sort, Video.published_at)
    if order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    videos = query.offset(skip).limit(size).all()
    return [
        {
            "video_id": v.video_id,
            "title": v.title,
            "description": v.description,
            "published_at": v.published_at,
            "thumbnail_url": v.thumbnail_url,
            "channel_title": v.channel_title
        } for v in videos
    ]

fetcher = YouTubeFetcher(SessionLocal)

@app.on_event("startup")
async def start_fetcher():
    asyncio.create_task(fetcher.fetch())
