# main.py

import json
import feedparser
import hashlib
import base64
from datetime import datetime
from pathlib import Path
import sys
from html_builder import build_index_html

FEEDS_FILE = "feeds.json"
OUTPUT_FILE = "index.html"

# --- Utility Functions ---

def generate_uniqueid(url):
    sha256_hash = hashlib.sha256(url.encode('utf-8')).digest()
    base64_hash = base64.urlsafe_b64encode(sha256_hash).decode('utf-8').rstrip('=')
    return base64_hash

# --- Core Functions ---

def load_feeds(file_path):
    if not Path(file_path).exists():
        print(f"ERROR: {file_path} not found.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_feeds(feeds):
    for feed in feeds:
        if "source" not in feed or "url" not in feed or "uniqueid" not in feed:
            print(f"ERROR: Feed entry missing required fields: {feed}")
            sys.exit(1)
        expected_id = generate_uniqueid(feed["url"])
        if feed["uniqueid"] != expected_id:
            print(f"ERROR: uniqueid mismatch for feed '{feed['source']}'. Expected: {expected_id}")
            sys.exit(1)

def fetch_articles(feeds):
    articles = []
    for feed in feeds:
        parsed_feed = feedparser.parse(feed["url"])
        for entry in parsed_feed.entries:
            published = ""
            if hasattr(entry, "published"):
                published = entry.published
            elif hasattr(entry, "updated"):
                published = entry.updated

            link = entry.link if hasattr(entry, "link") else ""
            title = entry.title if hasattr(entry, "title") else "No Title"

            articles.append({
                "date": published,
                "source": feed["source"],
                "source_id": feed["uniqueid"],
                "title": title,
                "link": link
            })
    return articles

# --- Main Execution ---

def main():
    feeds = load_feeds(FEEDS_FILE)
    validate_feeds(feeds)
    articles = fetch_articles(feeds)

    html_content = build_index_html(articles, feeds)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ {OUTPUT_FILE} generated successfully with {len(articles)} articles.")

if __name__ == "__main__":
    main()
