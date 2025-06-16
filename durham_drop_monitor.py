import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def check_durham_drop():
    url = "https://www.durhamabc.com/drops"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Durham ABC page: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Look for "Drop Available" to determine active drop
    drop_active = bool(soup(text=re.compile(r"drop available", re.I)))
    if drop_active:
        print("✅ A DROP IS CURRENTLY ACTIVE!")
    else:
        print("❌ No drop active.")

    # Find the most recent post title, date, and body
    post_section = soup.find("article")
    if not post_section:
        print("⚠️ Could not find post content.")
        return

    # Title
    title_tag = post_section.find(["h2", "h1"])
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    # Date
    date_tag = post_section.find(string=re.compile(r"posted on", re.I))
    if date_tag:
        match = re.search(r"posted on\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", date_tag, re.I)
        if match:
            post_date_str = match.group(1)
            try:
                post_date = datetime.strptime(post_date_str, "%B %d, %Y")
                days_ago = (datetime.now() - post_date).days
                date_summary = f"{post_date_str} ({days_ago} days ago)"
            except ValueError:
                date_summary = f"Unknown format: {post_date_str}"
        else:
            date_summary = "Date not found"
    else:
        date_summary = "No date text found"

    # Body
    body_tag = post_section.find("p")
    body_text = body_tag.get_text(strip=True) if body_tag else "No body content found"

    # Print summary
    print("\n📋 Most Recent Drop Info")
    print(f"Title: {title}")
    print(f"Posted: {date_summary}")
    print(f"Summary: {body_text}")

# Run only when this file is executed directly
if __name__ == "__main__":
    check_durham_drop()
