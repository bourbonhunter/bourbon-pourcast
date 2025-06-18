import requests
from bs4 import BeautifulSoup
import pdfkit
from datetime import datetime
from jinja2 import Template

SEARCH_TERMS = [
    "blanton", "old fitz", "eagle rare", "taylor", "weller", "stagg", "elmer"
]

BASE_URL = "https://wakeabc.com/search-our-inventory/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bourbon Pourcast Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; }
        h1 { color: #6c2e1f; }
        h3 { color: #8b4513; }
        ul { list-style-type: square; }
        .no-results { color: #888; }
        .logo { max-width: 200px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <img class="logo" src="https://bourbonpourcast.com/logo.png" alt="Bourbon Pourcast Logo">
    <h1>Bourbon Pourcast Inventory Report</h1>
    <p><strong>📅 Report generated:</strong> {{ timestamp }}</p>
    {{ results_section | safe }}
</body>
</html>
"""

def fetch_inventory():
    results = []
    for term in SEARCH_TERMS:
        response = requests.get(BASE_URL, params={"s": term}, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.select(".elementor-post")
        results.append(f"<h3>🔍 Searching for: {term}</h3>")
        if listings:
            results.append("<ul>")
            for item in listings:
                title = item.select_one(".elementor-post__title")
                location = item.select_one(".elementor-post__excerpt")
                if title and location:
                    results.append(f"<li><strong>{title.text.strip()}</strong><br>{location.text.strip()}</li>")
            results.append("</ul>")
        else:
            results.append(f"<p class='no-results'>❌ No results found.</p>")
    return "\n".join(results)

def save_results_as_files(rendered_html):
    with open("search_results.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)

    # Strip HTML for text version
    soup = BeautifulSoup(rendered_html, "html.parser")
    with open("search_results.txt", "w", encoding="utf-8") as f:
        f.write(soup.get_text())

    # Generate PDF
    pdfkit.from_file("search_results.html", "bourbon_report.pdf")

def main():
    print("🔍 Running bourbon inventory search...")
    results_section = fetch_inventory()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = Template(HTML_TEMPLATE).render(timestamp=timestamp, results_section=results_section)
    save_results_as_files(html)
    print("✅ All done! Reports saved.")

if __name__ == "__main__":
    main()
