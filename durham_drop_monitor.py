import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def get_latest_drop_info():
    url = "https://www.durhamabc.com/drops"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to load page: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the first blog post card
    post = soup.find("div", class_="sppb-addon-article")

    if not post:
        print("⚠️ Could not find post content.")
        return None

    title_tag = post.find("h3")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

    date_tag = post.find("small")
    date_text = date_tag.get_text(strip=True) if date_tag else "Unknown date"

    # Extract date from format like: "Published: 14 June 2024"
    date_match = re.search(r"Published:\s*(\d+\s+\w+\s+\d{4})", date_text)
    if date_match:
        post_date = datetime.strptime(date_match.group(1), "%d %B %Y")
        days_ago = (datetime.now() - post_date).days
    else:
        post_date = None
        days_ago = "?"

    # Get post summary text
    summary_tag = post.find("p")
    summary = summary_tag.get_text(strip=True) if summary_tag else "No summary found."

    drop_active = "drop" in title.lower() and "available" in title.lower()

    print("📝 Most Recent Drop Blog Post:")
    print(f"📅 Date: {post_date.strftime('%B %d, %Y') if post_date else 'Unknown'} ({days_ago} days ago)")
    print(f"🧾 Title: {title}")
    print(f"📄 Summary: {summary}")
    print(f"{'✅ Drop is ACTIVE!' if drop_active else '❌ No drop active.'}")

    return {
        "title": title,
        "date": post_date,
        "days_ago": days_ago,
        "summary": summary,
        "active": drop_active
    }

if __name__ == "__main__":
    get_latest_drop_info()
