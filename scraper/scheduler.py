# scraper/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from .scraper import scrape_all

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_all, 'interval', minutes=30)
    scheduler.start()
    print("🕒 Scraper scheduler started (every 30 minutes)")