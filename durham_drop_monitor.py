import requests
from bs4 import BeautifulSoup
import re

def fetch_durham_html():
    url = "https://www.durhamabc.com/drops"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"⚠️ Error fetching Durham drop page: {e}")
        return None

def extract_drop_info(html):
    soup = BeautifulSoup(html, "html.parser")

    # Try to extract drop text based on known format
    drop_text = None
    for div in soup.find_all("div"):
        text = div.get_text(strip=True)
        if re.search(r"Store\s+#\d+.*\d{4}", text):  # e.g. Store #1 ... 2025
            drop_text = text
            break

    # Look for a <span> with a title attribute like "4 days ago"
    time_ago = None
    for span in soup.find_all("span", title=True):
        if re.match(r"^\d+\s+(day|days|hour|hours)\s+ago$", span["title"]):
            time_ago = span["title"]
            break

    if not drop_text:
        print("❌ Could not locate drop description.")
        return None

    if not time_ago:
        print("❌ Could not locate drop date info.")
        return None

    return drop_text, time_ago

def main():
    html = fetch_durham_html()
    if not html:
        return

    with open("durham_debug.html", "w", encoding="utf-8") as f:
        f.write(html)
        print("✅ Saved HTML to durham_debug.html for inspection.")

    result = extract_drop_info(html)
    if result:
        drop_text, time_ago = result
        print(f"📍 Most Recent Drop:\n{drop_text}")
        print(f"🕒 Drop occurred: {time_ago}")
    else:
        print("❌ No drop info extracted.")

if __name__ == "__main__":
    main()
