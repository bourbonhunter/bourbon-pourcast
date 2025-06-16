import requests
from bs4 import BeautifulSoup

def fetch_latest_drop():
    url = "https://www.durhamabc.com/drops"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        # Find the drop description block
        drop_div = soup.find("div", class_="BOlnTh")
        drop_text = drop_div.get_text(strip=True) if drop_div else None

        # Find the "x days ago" text
        date_span = soup.find("span", class_="post-metadata__date")
        time_ago = date_span.get_text(strip=True) if date_span else None

        if drop_text:
            print("✅ Latest Durham Drop Found:")
            print(f"- Details: {drop_text}")
            print(f"- Posted: {time_ago}")
        else:
            print("❌ No drop info found.")

    except Exception as e:
        print(f"⚠️ Error extracting Durham drop details: {e}")

if __name__ == "__main__":
    fetch_latest_drop()
