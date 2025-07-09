import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEYS = os.getenv("YOUTUBE_API_KEYS", "").split(",")
SEARCH_QUERY = os.getenv("SEARCH_QUERY", "cricket")
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 10))
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:123456@localhost:3306/youtube_db")
