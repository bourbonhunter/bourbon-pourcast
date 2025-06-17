import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import pdfkit
from datetime import datetime

SEARCH_TERMS = [
    "blanton", "eagle rare", "eh taylor", "weller", "stagg", "elmer"
]

URL = "https://wakeabc.com/search-our-inventory/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
TXT_OUTPUT = "search_results.txt"
CSV_OUTPUT = "current_inventory.csv"
HTML_OUTPUT = "search_results.html"
PDF_OUTPUT = "bourbon_report.pdf"

def fetch_inventory():
    print("🔍 Running bourbon inventory search...")
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()
    return response.text

def parse_inventory(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    text_output = [f"📅 Report generated: {TIMESTAMP}\n"]

    for term in SEARCH_TERMS:
        text_output.append(f"\n🔍 Searching for: {term}")
        matches = soup.find_all(string=lambda s: s and term.lower() in s.lower())

        if matches:
            for match in matches:
                parent = match.find_parent()
                item_text = parent.get_text(strip=True) if parent else match
                results.append((term, item_text))
                text_output.append(f"✔️ {item_text}")
        else:
            text_output.append("❌ No results found.")

    return "\n".join(text_output), results

def save_txt(content):
    with open(TXT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)

def save_csv(data):
    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Search Term", "Matched Result"])
        writer.writerows(data)

def save_html(content):
    html_content = f"<html><body><pre>{content}</pre></body></html>"
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html_content)

def save_pdf():
    pdfkit.from_file(HTML_OUTPUT, PDF_OUTPUT)

def main():
    html = fetch_inventory()
    inventory_text, matches = parse_inventory(html)
    save_txt(inventory_text)
    save_csv(matches)
    save_html(inventory_text)
    save_pdf()
    print(f"✅ Results saved to:\n- {TXT_OUTPUT}\n- {CSV_OUTPUT}\n- {HTML_OUTPUT}\n- {PDF_OUTPUT}")

if __name__ == "__main__":
    main()
