# scraper/config.py

SOURCES = [
    {
        "name": "HackerNews",
        "url": "https://news.ycombinator.com/",
        "category": "Technology"
    },
    {
        "name": "BBC",
        "url": "https://www.bbc.com/news",
        "category": "News"
    },
    {
        "name": "CNN",
        "url": "https://edition.cnn.com",
        "category": "News"
    },
    {
        "name": "CoinDesk",
        "url": "https://www.coindesk.com",
        "category": "Crypto"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# How often scraper runs (scheduler)
SCRAPE_INTERVAL_MINUTES = 10

# Correct file path (IMPORTANT FIX)
DATA_FILE = "data/scraped_data.json"