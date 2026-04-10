# backend/services.py
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta

def load_data():
    try:
        with open("data/scraped_data.json", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def get_metrics():
    data = load_data()
    return {
        "total_items": len(data),
        "new_today": sum(1 for item in data if "2025" in item.get("scraped_at", "")),
        "sources": 5,
        "last_updated": "Just now"
    }

def get_categories():
    """Return live category breakdown with colors"""
    data = load_data()
    cat_count = Counter(item.get("category", "Other") for item in data)
    
    color_map = {
        "Technology": "#3b82f6",
        "Business": "#10b981",
        "Sports": "#f59e0b",
        "Health": "#8b5cf6",
        "Automotive": "#f59e0b",
        "Other": "#64748b"
    }
    
    categories = []
    for name, count in cat_count.most_common(5):
        categories.append({
            "name": name,
            "count": count,
            "color": color_map.get(name, "#64748b")
        })
    return categories

def get_trend_data():
    """Return real last 7 days trend"""
    data = load_data()
    today = datetime.now().date()
    daily = defaultdict(int)

    for item in data:
        if "scraped_at" in item:
            try:
                dt = datetime.fromisoformat(item["scraped_at"].split("+")[0])
                daily[dt.date()] += 1
            except:
                continue

    labels = []
    items_collected = []
    new_items = []   # for now we use same data for both lines

    for i in range(6, -1, -1):  # last 7 days
        d = today - timedelta(days=i)
        labels.append(d.strftime("%a"))
        count = daily.get(d, 0)
        items_collected.append(count)
        new_items.append(count)   # you can improve this later

    return {
        "labels": labels,
        "itemsCollected": items_collected,
        "newItems": new_items
    }