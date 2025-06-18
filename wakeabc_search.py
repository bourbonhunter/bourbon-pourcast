import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pdfkit
import os

SEARCH_TERMS = ["blanton", "old fitz", "eagle rare", "taylor", "weller", "stagg", "elmer"]

def fetch_inventory():
    base_url = "https://www.wakeabc.com/product-search"
    results = {}

    for term in SEARCH_TERMS:
        print(f"Searching for: {term}")
        params = {"q": term}
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.select(".product-container")
        if not items:
            results[term] = ["No results found."]
            continue

        term_results = []
        for item in items:
            name = item.select_one(".product-title").get_text(strip=True)
            stores_section = item.select_one(".inventory-toggle")
            if stores_section:
                stores = stores_section.get("data-stores", "")
                if stores:
                    store_list = [s.strip() for s in stores.split(",") if s.strip()]
                    term_results.append(f"{name} - Available at: {', '.join(store_list)}")
                else:
                    term_results.append(f"{name} - No store data.")
            else:
                term_results.append(f"{name} - Inventory not available.")
        results[term] = term_results
    return results

def generate_html(results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = ""
    for term, matches in results.items():
        rows += f"<h3>{term.title()}</h3>\n<ul>"
        for match in matches:
            rows += f"<li>{match}</li>"
        rows += "</ul>\n"
    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            h1 {{ color: #2c3e50; }}
            h3 {{ color: #34495e; }}
            ul {{ list-style-type: disc; padding-left: 20px; }}
        </style>
    </head>
    <body>
        <h1>Bourbon Pourcast Report</h1>
        <p>Report generated: {timestamp}</p>
        {rows}
    </body>
    </html>
    """

def save_files(results):
    html_content = generate_html(results)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt_lines = [f"Report generated: {timestamp}"]
    for term, matches in results.items():
        txt_lines.append(f"\n{term.title()}")
        txt_lines.extend(matches)

    with open("bourbon_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    with open("bourbon_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))

    pdfkit.from_file("bourbon_report.html", "bourbon_report.pdf")

def main():
    print("🔍 Running bourbon inventory search...")
    results = fetch_inventory()
    save_files(results)
    print("✅ Reports saved as TXT, HTML, and PDF.")

if __name__ == "__main__":
    main()
