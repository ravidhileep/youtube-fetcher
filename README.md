# FastAPI YouTube Search API

Fetch the **10 most recently‑published YouTube videos** for any search term via a simple JSON HTTP endpoint.

---

## ✨ Features

* **/search?q=term** – returns latest 10 videos, sorted by publish time
* Asynchronous HTTP client (`httpx.AsyncClient`) for non‑blocking I/O
* Secure API key handling via **environment variables / `.env`** (no secrets in source)
* Fully typed with clear error responses

---

## 🗂️ Project Structure

```
fastapi-youtube-search/
├── main.py          # FastAPI application
├── .env.example     # Example env file (copy → .env)
├── requirements.txt # Python dependencies
└── README.md        # This file
```

---

## 🚀 Quick Start

1. **Clone** the repo

   ```bash
   git clone https://github.com/<your-username>/fastapi-youtube-search.git
   cd fastapi-youtube-search
   ```

2. **Create & activate** a virtual environment (Windows PowerShell)

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

   <small>macOS/Linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   </small>

3. **Install** requirements

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Copy `.env.example` to `.env` and add your key:

   ```env
   YOUTUBE_API_KEY=YOUR_REAL_KEY_HERE
   ```

5. **Run** the development server

   ```bash
   uvicorn main:app --reload
   ```

   The API is now live at [http://127.0.0.1:8000](http://127.0.0.1:8000). Swagger docs are at `/docs`.

---

## 🔌 Endpoint

| Method | Path      | Query Params | Description                    |
| :----: | --------- | ------------ | ------------------------------ |
|   GET  | `/search` | `q` (string) | Returns latest 10 YouTube vids |

### Example Request

```http
GET /search?q=cricket HTTP/1.1
Host: 127.0.0.1:8000
```

### Example Response

```json
{
  "query": "cricket",
  "results": [
    {
      "title": "Match Highlights | IND vs ENG",
      "video_url": "https://www.youtube.com/watch?v=abc123",
      "published_at": "2025-07-13T07:15:02Z"
    },
    ... 9 more ...
  ]
}
```

If the YouTube API call fails, the endpoint returns:

```json
{
  "error": "Failed to fetch data from YouTube API"
}
```

---

## 🧩 Environment Variables

| Name              | Description                             |
| ----------------- | --------------------------------------- |
| `YOUTUBE_API_KEY` | Your YouTube Data API v3 key (required) |

> **Tip:** Rotate or restrict the key to this endpoint’s IP if deploying.



## 🙋 FAQ

### Q: Why use `httpx` instead of `requests`?

> `httpx` supports **async/await**, enabling high concurrency without extra threads.

### Q: How can I paginate more than 10 results?

> Adjust `maxResults` (up to 50) and manage `nextPageToken` values from the YouTube API response.

---
