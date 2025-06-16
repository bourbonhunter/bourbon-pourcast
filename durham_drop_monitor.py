import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

DROP_URL = "https://www.durhamabc.com/drops"
DEBUG_FILE = "durham_debug.html"

def fetch_drop_page():
    try:
        response = requests.get(DROP_URL)
        response.raise_for_status()
        html = response.text
        with open(DEBUG_FILE, "w", encoding="utf-8") as f:
            f.write(html)
        return html
    except Exception as e:
        print(f"❌ Failed to fetch Durham drop page: {e}")
        return None

def parse_drop_info(html):
    soup = BeautifulSoup(html, "html.parser")

    # Look for a span tag with a title like "4 days ago"
    time_tag = soup.find("span", title=re.compile(r"\d+ days? ago"))
    if not time_tag:
        print("❌ Could not locate drop timestamp.")
        return None

    days_ago = time_tag["title"]

    # Get the closest previous div containing drop description
    drop_text = None
    for parent in time_tag.parents:
        description_div = parent.find("div", class_=re.compile(r"BOlnTh"))
        if description_div:
            drop_text = description_div.get_text(strip=True)
            break

    if not drop_text:
        print("❌ Could not locate drop description.")
        return None

    return {
        "description": drop_text,
        "posted": days_ago
    }

def main():
    html = fetch_drop_page()
    if not html:
        return

    drop_info = parse_drop_info(html)
    if not drop_info:
        print("❌ No drop info extracted.")
        return

    print("✅ Drop Info:")
    print(f"📍 {drop_info['description']}")
    print(f"📅 Posted: {drop_info['posted']}")

if __name__ == "__main__":
    main()
