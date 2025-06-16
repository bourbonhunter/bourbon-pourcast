import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

URL = "https://www.durhamabc.com/drops"
DEBUG_FILE = "durham_debug.html"

def fetch_drop_page():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        html = response.text
        with open(DEBUG_FILE, "w", encoding="utf-8") as f:
            f.write(html)
        return html
    except Exception as e:
        print(f"⚠️ Error fetching page: {e}")
        return None

def extract_drop_info(html):
    soup = BeautifulSoup(html, "html.parser")

    # Look for any <span> element with a class that includes "post-metadata__date"
    time_span = soup.find("span", class_=lambda x: x and "post-metadata__date" in x)
    drop_text_div = soup.find("div", class_=lambda x: x and "blog-post-description-style-font" in x)

    if not drop_text_div:
        print("❌ Could not locate drop description.")
        return None

    if not time_span or not time_span.get("title"):
        print("❌ Could not locate drop date info.")
        return None

    drop_text = drop_text_div.get_text(strip=True)
    time_ago = time_span["title"]

    return drop_text, time_ago

def main():
    html = fetch_drop_page()
    if not html:
        return

    result = extract_drop_info(html)
    if result:
        drop_text, time_ago = result
        print(f"✅ Most Recent Drop: {drop_text}")
        print(f"🕒 Drop occurred: {time_ago}")
    else:
        print("❌ No drop info extracted.")

if __name__ == "__main__":
    main()
