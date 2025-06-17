import csv
import os
import pdfkit
from bs4 import BeautifulSoup
import requests
from jinja2 import Template

# Search terms
SEARCH_TERMS = [
    "weller", "blanton", "eh taylor", "elmer", "stagg",
    "eagle rare", "old fitz"
]

# Output files
TXT_OUTPUT = "search_results.txt"
CSV_OUTPUT = "current_inventory.csv"
HTML_OUTPUT = "search_results.html"
PDF_OUTPUT = "bourbon_report.pdf"

def fetch_inventory():
    print("🔍 Running bourbon inventory search...")
    url = "https://wakeabc.com/inventory"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_inventory(html, search_terms):
    soup = BeautifulSoup(html, "html.parser")
    inventory = []
    for row in soup.select("tr"):
        cols = row.find_all("td")
        if len(cols) >= 4:
            name = cols[0].get_text(strip=True).lower()
            for term in search_terms:
                if term in name:
                    inventory.append({
                        "name": cols[0].get_text(strip=True),
                        "price": cols[1].get_text(strip=True),
                        "size": cols[2].get_text(strip=True),
                        "inventory": cols[3].get_text(strip=True),
                    })
                    break
    return inventory

def save_txt(results, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for item in results:
            f.write(f"- {item['name']}\n")
            f.write(f"  Price: {item['price']} | Size: {item['size']}\n")
            f.write(f"  Inventory: {item['inventory']}\n\n")

def save_csv(results, filename):
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "size", "inventory"])
        writer.writeheader()
        writer.writerows(results)

def save_html(results, filename):
    template = Template("""
    <html>
    <head><meta charset="utf-8"><title>Bourbon Search Results</title></head>
    <body>
    <h1>Bourbon Search Results</h1>
    <ul>
    {% for item in results %}
        <li><strong>{{ item.name }}</strong><br>
        Price: {{ item.price }} | Size: {{ item.size }}<br>
        Inventory: {{ item.inventory }}</li>
    {% endfor %}
    </ul>
    </body>
    </html>
    """)
    html = template.render(results=results)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

def save_pdf(html_file, pdf_file):
    pdfkit.from_file(html_file, pdf_file)

def main():
    html = fetch_inventory()
    results = parse_inventory(html, SEARCH_TERMS)
    save_txt(results, TXT_OUTPUT)
    save_csv(results, CSV_OUTPUT)
    save_html(results, HTML_OUTPUT)
    save_pdf(HTML_OUTPUT, PDF_OUTPUT)
    print("✅ All searches complete. Results saved to:")
    print(f"- {TXT_OUTPUT}")
    print(f"- {CSV_OUTPUT}")
    print(f"- {HTML_OUTPUT}")
    print(f"- {PDF_OUTPUT}")

if __name__ == "__main__":
    main()
