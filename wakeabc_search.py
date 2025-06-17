import requests
from bs4 import BeautifulSoup
import pdfkit
from datetime import datetime

SEARCH_TERMS = [
    "blanton", "old fitz", "eagle rare", "taylor", "weller", "stagg", "elmer"
]

BASE_URL = "https://wakeabc.com/search-our-inventory/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_inventory():
    results = []
    for term in SEARCH_TERMS:
        response = requests.get(BASE_URL, params={"s": term}, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.select(".elementor-post")
        if listings:
            results.append(f"<h3>🔍 Searching for: {term}</h3><ul>")
            for item in listings:
                title = item.select_one(".elementor-post__title")
                location = item.select_one(".elementor-post__excerpt")
                if title and location:
                    results.append(f"<li><strong>{title.text.strip()}</strong><br>{location.text.strip()}</li>")
            results.append("</ul>")
        else:
            results.append(f"<h3>🔍 Searching for: {term}</h3><p>❌ No results found.</p>")
    return results

def save_results_as_files(html_results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_html = f"<html><body><h2>📅 Report generated: {timestamp}</h2>{''.join(html_results)}</body></html>"

    with open("search_results.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    with open("search_results.txt", "w", encoding="utf-8") as f:
        f.write(BeautifulSoup(full_html, "html.parser").get_text())

    pdfkit.from_file("search_results.html", "bourbon_report.pdf")

def main():
    print("🔍 Running bourbon inventory search...")
    html_results = fetch_inventory()
    save_results_as_files(html_results)
    print("✅ All done! Results saved.")

if __name__ == "__main__":
    main()
