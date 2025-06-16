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

    # Find all drop containers with the class that matches the known drop text
    # We look for something like: <div class="BOlnTh">Store #1 ...</div>
    store_divs = soup.find_all("div", class_="BOlnTh")
    if not store_divs:
        print("❌ Could not find any drop info.")
        return

    drop_text = store_divs[0].get_text(strip=True)

    # Try to find relative post date
    time_tag = soup.find("span", class_="post-metadata__date")
    relative_time = time_tag.get_text(strip=True) if time_tag else "Unknown"

    print(f"✅ Most Recent Drop: {drop_text}")
    print(f"📅 Posted: {relative_time}")

if __name__ == "__main__":
    fetch_drop_info()
