from fastapi import APIRouter
from scraper.scraper import scrape_all
import json
from datetime import datetime
from collections import Counter

router = APIRouter()

DATA_FILE = "data/scraped_data.json"


# =========================
# LOAD DATA
# =========================
def load_data():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except:
        return []


# =========================
# RUN SCRAPER
# =========================
@router.post("/run-scraper")
def run_scraper():
    try:
        data = scrape_all()
        return {
            "status": "success",
            "items_scraped": len(data)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# =========================
# LATEST DATA
# =========================
@router.get("/latest")
def get_latest():
    return load_data()


# =========================
# METRICS (WITH FALLBACK)
# =========================
@router.get("/metrics")
def get_metrics():
    data = load_data()

    if not data:
        return {
            "total_items": 0,
            "new_today": 0,
            "sources": 0,
            "last_updated": "No data"
        }

    return {
        "total_items": len(data),
        "new_today": len(data),
        "sources": len(set(item["source"] for item in data)),
        "last_updated": datetime.now().strftime("%H:%M:%S")
    }


# =========================
# TREND DATA (FAKE OK FOR NOW)
# =========================
@router.get("/trend")
def get_trend():
    return {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "itemsCollected": [5, 8, 6, 10, 7, 12, 9],
        "newItems": [2, 3, 2, 4, 3, 5, 4]
    }


# =========================
# CATEGORY DATA (WITH FALLBACK)
# =========================
@router.get("/categories")
def get_categories():
    data = load_data()

    if not data:
        return [
            {"name": "Technology", "count": 0, "color": "#3b82f6"},
            {"name": "News", "count": 0, "color": "#10b981"},
            {"name": "Crypto", "count": 0, "color": "#f59e0b"},
            {"name": "Sports", "count": 0, "color": "#ef4444"}
        ]

    counter = Counter(item["category"] for item in data)

    colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]

    result = []
    for i, (name, count) in enumerate(counter.items()):
        result.append({
            "name": name,
            "count": count,
            "color": colors[i % len(colors)]
        })

    return result


# =========================
# 🔥 TOP SOURCES (NEW)
# =========================
@router.get("/top-sources")
def get_top_sources():
    data = load_data()

    if not data:
        return [
            {"name": "HackerNews", "count": 0},
            {"name": "BBC", "count": 0},
            {"name": "CNN", "count": 0}
        ]

    counter = Counter(item["source"] for item in data)

    # Sort by most frequent
    top_sources = counter.most_common(5)

    return [
        {"name": name, "count": count}
        for name, count in top_sources
    ]