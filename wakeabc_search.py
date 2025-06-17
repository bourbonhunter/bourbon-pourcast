import requests
from bs4 import BeautifulSoup
import csv
import difflib
from fpdf import FPDF
import os
import base64

HTML_OUTPUT = "search_results.html"
TEXT_OUTPUT = "search_results.txt"
PDF_OUTPUT = "bourbon_report.pdf"
CSV_CURRENT = "current_inventory.csv"
CSV_PREVIOUS = "previous_inventory.csv"

FONT_NAME = "DejaVu"
FONT_B64 = """
AAEAAAAUAQAABABARkZUTaBPHiQAAAFMAAAAHEdERUaO7JTDAAABaAAAApJHUE9TVoDENQAAA/wAAJ6KR1NVQsHQQFkAAKKIAAAV3k1BVEinMjh9AAC4aAAABj5PUy8yWS12LQAAvqgAAABWY21hcPIJUy0AAL8AAAAbkGN2dCAAaR05AADakAAAAf5mcGdtcTR2agAA3JAAAACrZ2FzcAAHAAcAAN08AAAADGdseWYHIChAAADdSAAIgcRoZWFkJcTijAAJXwwAAAA2aGhlYQ2fH8sACV9EAAAAJGhtdHglotvnAAlfaAAAYZZrZXJuDJkIOwAJwQAAAD/8bG9jYWEgYcwACgD8AABhuG1heHAc2gZxAApitAAAACBuYW1lH29NowAKYtQAAD0IcG9zdEkillQACp/cAADyZHByZXA7B/EAAAuSQAAABWgAAAABAAAAAN/t5XUAAAAA4DCcVwAAAADgMJxXAAEAAAAMAAACJgIuAAIA
"""  # Base64-encoded DejaVuSans.ttf

def decode_and_save_font():
    font_data = base64.b64decode(FONT_B64)
    with open("DejaVuSans.ttf", "wb") as f:
        f.write(font_data)

def run_bourbon_search():
    # Sample stub data — replace with actual scraping logic
    results = [
        {"name": "E.H. Taylor Small Batch", "price": "39.99", "location": "Raleigh"},
        {"name": "Blanton's Single Barrel", "price": "64.95", "location": "Garner"},
    ]
    return results

def save_to_csv(filename, results):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "location"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def load_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def compare_deltas(current, previous):
    current_set = {f"{r['name']}|{r['location']}" for r in current}
    previous_set = {f"{r['name']}|{r['location']}" for r in previous}
    added = current_set - previous_set
    removed = previous_set - current_set
    return list(added), list(removed)

def format_deltas(added, removed):
    delta_text = "🆕 Items Added:\n"
    delta_text += "\n".join(f"  - {item}" for item in added) if added else "  None"
    delta_text += "\n\n❌ Items No Longer Available:\n"
    delta_text += "\n".join(f"  - {item}" for item in removed) if removed else "  None"
    return delta_text + "\n\n"

def save_text(filename, delta_text, inventory_text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(delta_text + inventory_text)

def save_html(filename, delta_text, results):
    html = "<html><head><meta charset='UTF-8'><title>Bourbon Report</title></head><body>"
    html += f"<h2>Inventory Delta</h2><pre>{delta_text}</pre><hr>"
    html += "<h2>Current Inventory</h2><ul>"
    for r in results:
        html += f"<li><strong>{r['name']}</strong> - ${r['price']} at {r['location']}</li>"
    html += "</ul></body></html>"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

def save_pdf(delta_text, inventory_text):
    decode_and_save_font()
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font(FONT_NAME, '', "DejaVuSans.ttf", uni=True)
    pdf.set_font(FONT_NAME, size=12)

    combined = delta_text + "\n" + inventory_text
    lines = combined.splitlines()
    for line in lines:
        pdf.multi_cell(0, 10, line)
    pdf.output(PDF_OUTPUT)

def generate_inventory_text(results):
    lines = []
    for r in results:
        lines.append(f"- {r['name']} (${r['price']}) — {r['location']}")
    return "\n".join(lines)

def main():
    print("🔍 Running bourbon inventory search...")
    current_results = run_bourbon_search()
    previous_results = load_csv(CSV_PREVIOUS)

    save_to_csv(CSV_CURRENT, current_results)

    added, removed = compare_deltas(current_results, previous_results)
    delta_text = format_deltas(added, removed)
    inventory_text = generate_inventory_text(current_results)

    save_text(TEXT_OUTPUT, delta_text, inventory_text)
    save_html(HTML_OUTPUT, delta_text, current_results)
    save_pdf(delta_text, inventory_text)

    os.replace(CSV_CURRENT, CSV_PREVIOUS)
    print("✅ All results generated and saved.")

if __name__ == "__main__":
    main()
