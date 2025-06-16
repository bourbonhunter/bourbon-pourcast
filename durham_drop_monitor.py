import requests
from bs4 import BeautifulSoup
import re

def fetch_drop_info():
    url = "https://www.durhamabc.com/drops"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"⚠️ Request failed: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Grab the first blog post container
    post_container = soup.select_one('[data-hook="post-list-container"] [data-hook="post-description"]')
    if not post_container:
        print("❌ Could not locate blog post container.")
        return

    # Extract drop text
    drop_text = post_container.get_text(strip=True)

    # Extract the relative post time from "4 days ago", etc.
    time_tag = soup.select_one(".post-metadata__date")
    relative_time = time_tag.get_text(strip=True) if time_tag else "Unknown"

    print(f"✅ Most Recent Drop: {drop_text}")
    print(f"📅 Posted: {relative_time}")

if __name__ == "__main__":
    fetch_drop_info()
