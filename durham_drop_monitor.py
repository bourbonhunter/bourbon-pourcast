import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

BASE_URL = "https://www.durhamabc.com"
DROP_PAGE = f"{BASE_URL}/drops"

def fetch_drop_page():
    try:
        response = requests.get(DROP_PAGE)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Error fetching drop page: {e}")
        return None

def find_latest_post_url(html):
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "drop-available" in href:
            full_url = urljoin(BASE_URL, href)
            print(f"🔗 Found drop link: {full_url}")
            return full_url
    print("⚠️ No matching <a> tag found with 'drop-available' in href.")
    return None

def fetch_post_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Error fetching post content: {e}")
        return None

def extract_drop_info(html):
    soup = BeautifulSoup(html, "html.parser")

    # Drop description block (may require adjustment if class names change)
    drop_desc = soup.find("div", class_="BOlnTh")
    if not drop_desc:
        print("❌ Could not locate drop description.")
        return None

    drop_text = drop_desc.get_text(strip=True)

    # Days ago (optional display)
    days_ago_span = soup.find("span", class_="post-metadata__date")
    days_ago = days_ago_span.get_text(strip=True) if days_ago_span else "?"

    return {
        "description": drop_text,
        "days_ago": days_ago
    }

def main():
    print("🔍 Checking for latest Durham drop...")
    main_page = fetch_drop_page()
    if not main_page:
        return

    post_url = find_latest_post_url(main_page)
    if not post_url:
        return

    post_html = fetch_post_content(post_url)
    if not post_html:
        return

    drop_info = extract_drop_info(post_html)
    if not drop_info:
        print("❌ No drop info extracted.")
        return

    print("✅ Latest Drop Info:")
    print(f"🛒 {drop_info['description']}")
    print(f"📅 Posted: {drop_info['days_ago']} ago")

if __name__ == "__main__":
    main()
