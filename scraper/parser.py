# scraper/parser.py

import json
import os

DATA_FILE = "data/scraped_data.json"


def save_scraped_data(data):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)