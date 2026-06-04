import json 
from pathlib import Path 

import requests 
from dotenv import load_dotenv
import os

load_dotenv()

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN", "support.optisigns.com")
ARTICLE_LIMIT = 30

def fetch_articles():
    url = f"https://{ZENDESK_SUBDOMAIN}/api/v2/help_center/en-us/articles.json"
    articles = []

    while url and len(articles) < ARTICLE_LIMIT:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        articles.extend(data.get("articles", []))

        url = data.get("next_page")

    return articles[:ARTICLE_LIMIT]

def save_articles(articles, output_dir=RAW_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)

    for article in articles:
        article_id = article["id"]
        file_path = output_dir / f"{article_id}.json"

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(article, file, ensure_ascii=False, indent=2)

    print(f"Saved {len(articles)} raw articles to {output_dir}")

if __name__ == "__main__":
    articles = fetch_articles()
    save_articales(articles)
