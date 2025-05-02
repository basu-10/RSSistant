import os
import pandas as pd
import feedparser
import requests
from config.settings import CSV_DIR, USER_AGENT

def load_feeds():
    feeds = {}
    for file in os.listdir(CSV_DIR):
        if file.endswith(".csv"):
            category = file.replace(".csv", "").lower()
            try:
                df = pd.read_csv(os.path.join(CSV_DIR, file))
                feeds[category] = df.to_dict("records")
            except Exception as e:
                print(f"[ERROR] Failed to load {file}: {e}")
    return feeds

valid_feeds = load_feeds()

def fetch_rss_feed(url):
    try:
        res = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=10)
        res.raise_for_status()
        feed = feedparser.parse(res.text)
        return feed if not feed.bozo else None
    except Exception as e:
        print(f"[ERROR] {url}: {e}")
        return None
