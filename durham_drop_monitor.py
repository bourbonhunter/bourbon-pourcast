import requests
from bs4 import BeautifulSoup

def check_durham_drop():
    try:
        url = "https://www.durhamabc.com/drops"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Search the whole page text for "Drop Available"
        full_text = soup.get_text(separator=' ', strip=True)

        if "Drop Available" in full_text:
            print("✅ Drop is ACTIVE!")
            snippet = full_text.split("Drop Available")[1][:200]
            print("Preview:", "Drop Available" + snippet + "...")
            return True
        else:
            print("❌ No drop active.")
            return False

    except Exception as e:
        print(f"⚠️ Error checking Durham drop: {e}")
        return False

if __name__ == "__main__":
    check_durham_drop()
