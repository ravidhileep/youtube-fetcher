import aiohttp
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .config import YOUTUBE_API_KEYS, SEARCH_QUERY, FETCH_INTERVAL
from .models import Video
from .crud import get_video_by_id, add_video

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

class YouTubeFetcher:
    def __init__(self, db_session_maker):
        self.db_session_maker = db_session_maker
        self.api_keys = [k.strip() for k in YOUTUBE_API_KEYS if k.strip()]
        self.key_index = 0
        self.last_published_at = (datetime.utcnow() - timedelta(days=1)).isoformat("T") + "Z"

    async def fetch(self):
        params = {
            "part": "snippet",
            "q": SEARCH_QUERY,
            "type": "video",
            "order": "date",
            "publishedAfter": self.last_published_at,
            "maxResults": 10,
            "key": self.api_keys[self.key_index]
        }
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(YOUTUBE_SEARCH_URL, params=params) as resp:
                        data = await resp.json()
                        if "error" in data:
                            if data["error"]["errors"][0].get("reason") == "quotaExceeded":
                                self.key_index = (self.key_index + 1) % len(self.api_keys)
                                params["key"] = self.api_keys[self.key_index]
                                print("Switched API key due to quota.")
                                await asyncio.sleep(2)
                                continue
                            else:
                                print(data["error"])
                                break

                        items = data.get("items", [])
                        if items:
                            print(f"Fetched {len(items)} new videos.")
                            db = self.db_session_maker()
                            for item in items:
                                vid = item["id"]["videoId"]
                                if get_video_by_id(db, vid):
                                    continue
                                snippet = item["snippet"]
                                video = Video(
                                    video_id=vid,
                                    title=snippet["title"],
                                    description=snippet.get("description", ""),
                                    published_at=datetime.strptime(snippet["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"),
                                    thumbnail_url=snippet["thumbnails"]["default"]["url"],
                                    channel_title=snippet.get("channelTitle", "")
                                )
                                add_video(db, video)
                                self.last_published_at = snippet["publishedAt"]
                            db.close()
                        await asyncio.sleep(FETCH_INTERVAL)
                except Exception as e:
                    print(f"Error: {e}")
                    await asyncio.sleep(FETCH_INTERVAL)
