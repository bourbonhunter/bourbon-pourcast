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

        # Try to find the drop announcement
        drop = soup.find("div", class_="sqs-block-content")
        text = drop.get_text(strip=True)

        if "Drop Available" in text:
            print("✅ Drop is ACTIVE!")
            print(text)
            return True
        else:
            print("❌ No drop active.")
            return False

    except Exception as e:
        print(f"⚠️ Error checking Durham drop: {e}")
        return False

if __name__ == "__main__":
    check_durham_drop()
