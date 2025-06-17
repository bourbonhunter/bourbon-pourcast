import csv
import os
import datetime
from fpdf import FPDF

SEARCH_TERMS = ["blanton", "old fitz", "weller", "taylor"]
TXT_OUTPUT = "search_results.txt"
HTML_OUTPUT = "search_results.html"
PDF_OUTPUT = "bourbon_report.pdf"
CSV_CURRENT = "current_inventory.csv"
CSV_PREVIOUS = "previous_inventory.csv"
FONT_NAME = "DejaVu"
FONT_FILE = "DejaVuSans.ttf"

def fetch_inventory():
    # Dummy data for demonstration
    return [
        {"name": "Weller Special Reserve", "price": "24.99", "stock": 5},
        {"name": "Michter's US*1", "price": "39.99", "stock": 3},
        {"name": "Elijah Craig Barrel Proof", "price": "79.99", "stock": 0}
    ]

def save_csv(data, filename):
    with open(filename, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "stock"])
        writer.writeheader()
        writer.writerows(data)

def load_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def compare_inventory(current, previous):
    current_set = {row["name"]: row for row in current}
    previous_set = {row["name"]: row for row in previous}

    added = [v for k, v in current_set.items() if k not in previous_set]
    removed = [v for k, v in previous_set.items() if k not in current_set]

    return added, removed

def format_inventory(inventory):
    lines = []
    for item in inventory:
        stock = f'{item["stock"]} in stock' if int(item["stock"]) > 0 else "Not Available"
        lines.append(f'- {item["name"]}\n  Price: {item["price"]} USD | Inventory: {stock}')
    return "\n".join(lines)

def save_txt(content):
    with open(TXT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)

def save_html(content):
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(f"<pre>{content}</pre>")

def save_pdf(delta_text, inventory_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font(FONT_NAME, "", FONT_FILE, uni=True)
    pdf.set_font(FONT_NAME, size=10)
    pdf.multi_cell(0, 10, delta_text + "\n\n" + inventory_text)
    pdf.output(PDF_OUTPUT)

def main():
    print("🔍 Running bourbon inventory search...")

    current_inventory = fetch_inventory()
    previous_inventory = load_csv(CSV_PREVIOUS)

    added, removed = compare_inventory(current_inventory, previous_inventory)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    delta_text = f"📈 Report Date: {now}\n"
    delta_text += f"🔍 Search Terms: {', '.join(SEARCH_TERMS)}\n\n"

    if added:
        delta_text += "✅ New Items Added:\n" + format_inventory(added) + "\n\n"
    else:
        delta_text += "✅ New Items Added: None\n\n"

    if removed:
        delta_text += "❌ Items Removed:\n" + format_inventory(removed) + "\n\n"
    else:
        delta_text += "❌ Items Removed: None\n\n"

    inventory_text = "📦 Full Inventory:\n" + format_inventory(current_inventory)

    final_text = delta_text + inventory_text

    save_txt(final_text)
    save_html(final_text)
    save_pdf(delta_text, inventory_text)
    save_csv(current_inventory, CSV_CURRENT)

    # Replace old CSV
    os.replace(CSV_CURRENT, CSV_PREVIOUS)
    print("✅ Report generated and saved.")

if __name__ == "__main__":
    main()
