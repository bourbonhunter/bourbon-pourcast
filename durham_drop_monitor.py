import requests
from bs4 import BeautifulSoup
import datetime

URL = "https://www.durhamabc.com/drops"
DEBUG_HTML = "durham_debug.html"

def get_drop_info():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error fetching page: {e}")
        return None

    # Save debug copy
    with open(DEBUG_HTML, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"✅ Saved HTML to {DEBUG_HTML} for inspection.")

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the latest blog post container
    drop_container = soup.find("div", class_="BOlnTh")
    date_container = soup.find("span", class_="post-metadata__date")

    if not drop_container or not date_container:
        print("❌ Could not find drop content or date.")
        return None

    drop_text = drop_container.get_text(strip=True)
    posted_ago = date_container.get_text(strip=True)

    return drop_text, posted_ago

if __name__ == "__main__":
    result = get_drop_info()
    if result:
        drop_text, posted_ago = result
        print(f"📢 Latest Drop Info:\n- {drop_text}\n- Posted: {posted_ago}")
    else:
        print("⚠️ No drop info found.")
