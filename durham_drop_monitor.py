import requests
from bs4 import BeautifulSoup

URL = "https://www.durhamabc.com/drops"

def fetch_drop_page():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        html = response.text

        # Save HTML for debugging
        with open("durham_debug.html", "w", encoding="utf-8") as f:
            f.write(html)

        print("✅ Saved HTML to durham_debug.html for inspection.")
        print("🕵️ Parsing skipped until we review durham_debug.html")

    except Exception as e:
        print(f"❌ Error fetching Durham drop page: {e}")

if __name__ == "__main__":
    fetch_drop_page()
