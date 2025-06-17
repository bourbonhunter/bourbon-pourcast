import csv
import os
from fpdf import FPDF
from datetime import datetime

TXT_OUTPUT = "search_results.txt"
HTML_OUTPUT = "search_results.html"
PDF_OUTPUT = "bourbon_report.pdf"
CURRENT_CSV = "current_inventory.csv"
PREVIOUS_CSV = "previous_inventory.csv"
FONT_PATH = "DejaVuSans.ttf"
FONT_NAME = "DejaVu"

def run_bourbon_search():
    # Simulated data for testing
    return [
        {"name": "Eagle Rare", "price": "34.95", "inventory": 15},
        {"name": "Blanton's", "price": "64.95", "inventory": 8},
        {"name": "Elmer T. Lee", "price": "39.95", "inventory": 0}
    ]

def save_to_csv(filename, data):
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "inventory"])
        writer.writeheader()
        writer.writerows(data)

def load_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def compute_delta(current, previous):
    current_names = {item['name'] for item in current}
    previous_names = {item['name'] for item in previous}

    added = current_names - previous_names
    removed = previous_names - current_names

    added_items = [item for item in current if item['name'] in added]
    removed_items = [item for item in previous if item['name'] in removed]

    return added_items, removed_items

def format_inventory_text(data):
    return "\n".join(
        f"- {item['name']} | ${item['price']} | Inventory: {item['inventory']}"
        for item in data
    )

def save_txt(filename, delta_text, inventory_text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(delta_text + "\n\n" + inventory_text)

def save_html(filename, delta_text, inventory_text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("<html><body>")
        f.write(f"<h2>Delta Report</h2><pre>{delta_text}</pre>")
        f.write(f"<h2>Current Inventory</h2><pre>{inventory_text}</pre>")
        f.write("</body></html>")

def save_pdf(delta_text, inventory_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font(FONT_NAME, '', FONT_PATH, uni=True)
    pdf.set_font(FONT_NAME, '', 12)
    pdf.multi_cell(0, 10, delta_text + "\n\n" + inventory_text)
    pdf.output(PDF_OUTPUT)

def main():
    print("🔍 Running bourbon inventory search...")
    current_inventory = run_bourbon_search()
    previous_inventory = load_csv(PREVIOUS_CSV)

    save_to_csv(CURRENT_CSV, current_inventory)
    added, removed = compute_delta(current_inventory, previous_inventory)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    delta_text = f"🕒 Report Generated: {timestamp}\n"
    delta_text += "\n📈 Items Added:\n" + ("\n".join(f"- {item['name']}" for item in added) or "None")
    delta_text += "\n\n📉 Items Removed:\n" + ("\n".join(f"- {item['name']}" for item in removed) or "None")

    inventory_text = format_inventory_text(current_inventory)

    save_txt(TXT_OUTPUT, delta_text, inventory_text)
    save_html(HTML_OUTPUT, delta_text, inventory_text)
    save_pdf(delta_text, inventory_text)

    # Replace previous with current
    os.replace(CURRENT_CSV, PREVIOUS_CSV)

    print(f"✅ All searches complete. Results saved to:\n- {TXT_OUTPUT}\n- {HTML_OUTPUT}\n- {PDF_OUTPUT}")

if __name__ == "__main__":
    main()
