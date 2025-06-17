import os
import csv
from datetime import datetime
from fpdf import FPDF
from bs4 import BeautifulSoup
import requests

# Constants
CURRENT_CSV = "current_inventory.csv"
PREVIOUS_CSV = "previous_inventory.csv"
TXT_OUTPUT = "search_results.txt"
HTML_OUTPUT = "search_results.html"
PDF_OUTPUT = "bourbon_report.pdf"
DELTA_OUTPUT = "delta.txt"

SEARCH_TERMS = ["elijah craig", "michter", "blue note"]

def fetch_inventory():
    # Simulated HTML response parsing
    return [
        {"name": "MICHTER'S 10Y SINGLE BARREL", "price": "$199.95", "location": "Cary", "stock": 33},
        {"name": "MICHTER'S SOUR MASH", "price": "$8.25", "location": "Raleigh", "stock": 0},
        {"name": "BLUE NOTE", "price": "$65.00", "location": "Garner", "stock": 4}
    ]

def save_csv(filename, items):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "location", "stock"])
        writer.writeheader()
        writer.writerows(items)

def load_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def compare_inventory(new, old):
    new_set = set((i["name"], i["location"]) for i in new if int(i["stock"]) > 0)
    old_set = set((i["name"], i["location"]) for i in old if int(i["stock"]) > 0)

    added = new_set - old_set
    removed = old_set - new_set
    return added, removed

def format_inventory(items):
    return "\n".join(
        f"- {item['name']} at {item['location']} (${item['price']}) — {item['stock']} in stock"
        for item in items
    )

def format_delta(added, removed):
    lines = []
    if added:
        lines.append("🟢 Items Added:")
        for name, loc in added:
            lines.append(f"  + {name} at {loc}")
    if removed:
        lines.append("\n🔴 Items Removed:")
        for name, loc in removed:
            lines.append(f"  - {name} at {loc}")
    return "\n".join(lines) or "No changes since last run."

def save_txt(content):
    with open(TXT_OUTPUT, "w") as f:
        f.write(content)

def save_html(content):
    html = f"<html><body><pre>{content}</pre></body></html>"
    with open(HTML_OUTPUT, "w") as f:
        f.write(html)

def save_pdf(delta_text, inventory_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    for line in delta_text.splitlines():
        pdf.cell(200, 10, line, ln=True)
    pdf.ln(10)
    for line in inventory_text.splitlines():
        pdf.cell(200, 10, line, ln=True)

    pdf.output(PDF_OUTPUT)

def main():
    print("🔍 Running bourbon inventory search...")

    inventory = fetch_inventory()
    save_csv(CURRENT_CSV, inventory)

    prev_inventory = load_csv(PREVIOUS_CSV)
    added, removed = compare_inventory(inventory, prev_inventory)

    delta_text = format_delta(added, removed)
    inventory_text = format_inventory(inventory)

    combined_text = f"{delta_text}\n\n📦 Full Inventory:\n{inventory_text}"

    save_txt(combined_text)
    save_html(combined_text)
    save_pdf(delta_text, inventory_text)

    save_csv(PREVIOUS_CSV, inventory)

    print("✅ All reports generated and saved.")

if __name__ == "__main__":
    main()
