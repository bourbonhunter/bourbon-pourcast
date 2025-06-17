import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
from fpdf import FPDF

SEARCH_TERMS = ["weller", "blanton", "e.h. taylor", "stag", "michter", "elijah craig", "booker", "george t. stagg", "blue note", "russell"]
BASE_URL = "https://www.wakeabc.com/retail-stores"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M")

CURRENT_FILE = "current_inventory.csv"
PREVIOUS_FILE = "previous_inventory.csv"
TXT_OUTPUT = "search_results.txt"
HTML_OUTPUT = "search_results.html"
PDF_OUTPUT = "bourbon_report.pdf"

def fetch_inventory():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    items = []
    for row in soup.select("tr"):
        cells = row.find_all("td")
        if len(cells) >= 3:
            name = cells[0].text.strip().lower()
            if any(term in name for term in SEARCH_TERMS):
                price = cells[1].text.strip()
                inventory = cells[2].text.strip()
                items.append([name, price, inventory])
    return items

def save_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Price", "Inventory"])
        writer.writerows(data)

def load_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        return list(reader)

def compute_deltas(current, previous):
    current_set = set(tuple(row) for row in current)
    previous_set = set(tuple(row) for row in previous)
    added = current_set - previous_set
    removed = previous_set - current_set
    return sorted(added), sorted(removed)

def format_deltas(added, removed):
    lines = []
    lines.append(f"🕒 Report generated: {TIMESTAMP}")
    lines.append(f"🔼 Items added since last report: {len(added)}")
    for item in added:
        lines.append(f"    + {item[0]} | {item[1]} | {item[2]}")
    lines.append(f"🔽 Items removed since last report: {len(removed)}")
    for item in removed:
        lines.append(f"    - {item[0]} | {item[1]} | {item[2]}")
    lines.append("\n")
    return "\n".join(lines)

def format_inventory(inventory):
    lines = []
    for item in inventory:
        lines.append(f"{item[0]} | {item[1]} | {item[2]}")
    return "\n".join(lines)

def save_txt(delta_text, inventory_text):
    with open(TXT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(delta_text)
        f.write(inventory_text)

def save_html(delta_text, inventory_text):
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write("<html><body>")
        f.write("<pre>")
        f.write(delta_text + "\n")
        f.write(inventory_text)
        f.write("</pre></body></html>")

def save_pdf(delta_text, inventory_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=10)
    for line in delta_text.split("\n") + inventory_text.split("\n"):
        pdf.cell(200, 6, txt=line, ln=True)
    pdf.output(PDF_OUTPUT)

def main():
    print("🔍 Running bourbon inventory search...")
    current_data = fetch_inventory()
    previous_data = load_csv(PREVIOUS_FILE)
    save_csv(current_data, CURRENT_FILE)

    added, removed = compute_deltas(current_data, previous_data)
    delta_text = format_deltas(added, removed)
    inventory_text = format_inventory(current_data)

    save_txt(delta_text, inventory_text)
    save_html(delta_text, inventory_text)
    save_pdf(delta_text, inventory_text)

    os.replace(CURRENT_FILE, PREVIOUS_FILE)
    print("✅ All searches complete. Results saved to:")
    print(f"- {TXT_OUTPUT}")
    print(f"- {HTML_OUTPUT}")
    print(f"- {PDF_OUTPUT}")

if __name__ == "__main__":
    main()
