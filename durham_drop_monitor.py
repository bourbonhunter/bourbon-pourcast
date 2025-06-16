import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.durhamabc.com"
DROPS_URL = f"{BASE_URL}/drops"
DEBUG_FILE = "durham_debug.html"

def fetch_drops_page():
    try:
        response = requests.get(DROPS_URL)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Error fetching drops page: {e}")
        return None

def find_latest_post_url(html):
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        if a["href"].startswith("/post/drop-available"):
            return BASE_URL + a["href"]
    return None

def fetch_post_page(post_url):
    try:
        response = requests.get(post_url)
        response.raise_for_status()
        with open(DEBUG_FILE, "w", encoding="utf-8") as f:
            f.write(response.text)
        return response.text
    except Exception as e:
        print(f"❌ Error fetching post page: {e}")
        return None

def extract_post_content(html):
    soup = BeautifulSoup(html, "html.parser")

    # Drop description (looks like "Store #1 1928 Holloway Street...")
    drop_div = soup.find("div", class_=re.compile(r"BOlnTh"))
    drop_text = drop_div.get_text(strip=True) if drop_div else None

    # Posted date (from span title, like "4 days ago")
    time_span = soup.find("span", title=re.compile(r"\d+ (day|hour)s? ago"))
    posted = time_span["title"] if time_span else None

    if not drop_text:
        print("❌ Could not locate drop description.")
    if not posted:
        print("❌ Could not locate drop age.")
    if drop_text and posted:
        return {"description": drop_text, "posted": posted}
    return None

def main():
    print("🔍 Checking for latest Durham drop...")

    drops_html = fetch_drops_page()
    if not drops_html:
        return

    post_url = find_latest_post_url(drops_html)
    if not post_url:
        print("❌ Could not locate post URL.")
        return

    print(f"🔗 Latest drop post URL: {post_url}")
    post_html = fetch_post_page(post_url)
    if not post_html:
        return

    info = extract_post_content(post_html)
    if info:
        print("\n✅ Durham Drop Found:")
        print(f"📍 {info['description']}")
        print(f"🕒 Posted: {info['posted']}")
    else:
        print("❌ No drop info extracted.")

if __name__ == "__main__":
    main()
