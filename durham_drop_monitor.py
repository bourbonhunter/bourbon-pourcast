import requests
from bs4 import BeautifulSoup
from datetime import datetime
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

    # Look for the div that contains drop info (typically post content)
    drop_text_div = soup.find("div", string=re.compile("Store #\\d+", re.IGNORECASE))
    if not drop_text_div:
        print("❌ No drop info found.")
        return

    drop_text = drop_text_div.get_text(strip=True)
    print(f"✅ Drop Info Found: {drop_text}")

    # Now try to extract relative time like "4 days ago"
    time_tag = soup.find("span", {"class": "post-metadata__date"})
    if time_tag:
        relative_time = time_tag.get_text(strip=True)
        print(f"📅 Posted: {relative_time}")
    else:
        print("⚠️ Could not determine how many days ago it was posted.")

if __name__ == "__main__":
    fetch_drop_info()
