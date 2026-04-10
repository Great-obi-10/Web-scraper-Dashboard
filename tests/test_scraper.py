# tests/test_scraper.py
from scraper.scraper import scrape_all

def test_scraper():
    count = scrape_all()
    assert count >= 0