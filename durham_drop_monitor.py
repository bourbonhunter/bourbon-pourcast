import requests
from bs4 import BeautifulSoup

def main():
    url = "https://www.durhamabc.com/drops"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch page: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # 🔍 Write HTML to file for inspection
    try:
        with open("durham_debug.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print("✅ Saved HTML to durham_debug.html for inspection.")
    except Exception as e:
        print(f"❌ Failed to write debug HTML: {e}")
        return

    # Placeholder for parsing logic until we verify HTML structure
    print("🕵️ Parsing skipped until we review durham_debug.html")

if __name__ == "__main__":
    main()
