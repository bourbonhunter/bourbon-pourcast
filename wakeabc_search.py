
import os
import csv
import time
import pdfkit
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SEARCH_TERMS = [
    "blanton", "old fitz", "eagle rare", "taylor", "weller", "stagg", "elmer"
]

OUTPUT_TXT = "bourbon_report.txt"
OUTPUT_HTML = "bourbon_report.html"
OUTPUT_PDF = "bourbon_report.pdf"

BASE_URL = "https://www.wakeabc.com/"
INVENTORY_URL = "https://www.wakeabc.com/Our-Stores/Search-Inventory"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

def fetch_inventory(term):
    session = requests.Session()
    session.headers.update(HEADERS)

    response = session.post(
        INVENTORY_URL,
        data={"q": term},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    table = soup.find("table", class_="abc-inventory")
    if not table:
        return results

    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue
        product = cols[0].get_text(strip=True)
        size = cols[1].get_text(strip=True)
        price = cols[2].get_text(strip=True)
        store = cols[3].get_text(strip=True)
        quantity = cols[4].get_text(strip=True)
        results.append((product, size, price, store, quantity))
    return results

def generate_reports(results_by_term):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt_lines = [f"Report generated: {timestamp}
"]
    html_lines = [
        f"<html><head><meta charset='UTF-8'><title>Bourbon Report</title></head><body>",
        f"<h1>Bourbon Pourcast Report</h1><p>Generated: {timestamp}</p>"
    ]

    for term, results in results_by_term.items():
        txt_lines.append(f"
Searching for: {term}")
        html_lines.append(f"<h2>Results for: {term}</h2>")
        if not results:
            txt_lines.append("No results found.")
            html_lines.append("<p>No results found.</p>")
            continue
        for product, size, price, store, quantity in results:
            txt_lines.append(f"{product} | {size} | {price} | {store} | {quantity}")
            html_lines.append(f"<p>{product} | {size} | {price} | {store} | {quantity}</p>")

    html_lines.append("</body></html>")

    # Save TXT
    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write("
".join(txt_lines))

    # Save HTML
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write("
".join(html_lines))

    # Save PDF using wkhtmltopdf
    pdfkit.from_file(OUTPUT_HTML, OUTPUT_PDF)

def main():
    print("🔍 Running bourbon inventory search...")
    results_by_term = {}
    for term in SEARCH_TERMS:
        print(f"Searching for: {term}")
        results = fetch_inventory(term)
        results_by_term[term] = results
        time.sleep(1)
    generate_reports(results_by_term)
    print("✅ Reports generated.")

if __name__ == "__main__":
    main()
