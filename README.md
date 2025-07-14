# FastAPI YouTube Search API

Fetch the **10 most recently‑published YouTube videos** for any search term via a simple JSON HTTP endpoint.

---

## ✨ Features

* Endpoint to search for the latest 10 YouTube videos
* Asynchronous HTTP requests for better performance
* Secure API key handling using environment variables
* Automatically generated API docs via FastAPI

---

## 🗂️ Project Structure

```
fastapi-youtube-search/
├── main.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

1. Clone the repository to your local machine.
2. Create a virtual environment and activate it.
3. Install the dependencies listed in `requirements.txt`.
4. Copy `.env.example` to `.env` and add your YouTube API key.
5. Run the FastAPI app using a development server.

---

## 🔌 Endpoint

* `/search?q=your_query_term`: Returns a JSON object with the latest 10 videos related to the search term.

---

## 🧩 Environment Variables

* `YOUTUBE_API_KEY`: Required. Your YouTube Data API v3 key.



## 🙋 FAQ

* **Why use `httpx` instead of `requests`?**
  Because `httpx` supports asynchronous requests which are more efficient in FastAPI.

* **How can I paginate more than 10 results?**
  Adjust `maxResults` and use `nextPageToken` from the YouTube API response.

---

Happy hacking! 🎉
