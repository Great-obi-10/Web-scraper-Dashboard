# scraper/scraper.py

import requests
from bs4 import BeautifulSoup
from .config import SOURCES, HEADERS
from .parser import save_scraped_data


def scrape_all():
    all_items = []

    for source in SOURCES:
        try:
            print(f"Scraping {source['name']}...")

            resp = requests.get(
                source["url"],
                headers=HEADERS,
                timeout=20  # ✅ increased timeout
            )

            soup = BeautifulSoup(resp.text, "html.parser")

            # Get all links (better than h2/h3)
            articles = soup.find_all("a", href=True)[:20]

            for article in articles:
                title = article.get_text(strip=True)

                if not title or len(title) < 15:
                    continue

                link = article["href"]

                # Fix relative URLs
                if link.startswith("/"):
                    link = source["url"].rstrip("/") + link

                all_items.append({
                    "id": len(all_items),
                    "title": title[:120],
                    "source": source["name"],
                    "category": source["category"],
                    "url": link
                })

        except Exception as e:
            print(f"❌ Error scraping {source['name']}: {e}")

    print(f"✅ Total items scraped: {len(all_items)}")

    # ✅ Prevent crash when saving
    try:
        save_scraped_data(all_items)
    except Exception as e:
        print("❌ Error saving data:", e)

    return all_items