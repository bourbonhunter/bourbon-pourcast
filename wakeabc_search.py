import os
import csv
from datetime import datetime
from fpdf import FPDF

# Constants
CURRENT_CSV = "current_inventory.csv"
PREVIOUS_CSV = "previous_inventory.csv"
TXT_OUTPUT = "search_results.txt"
HTML_OUTPUT = "search_results.html"
PDF_OUTPUT = "bourbon_report.pdf"

def mock_bourbon_search():
    # Replace with actual scraping logic as needed
    return [
        {"name": "E.H. Taylor Small Batch", "location": "Garner", "stock": 12},
        {"name": "Blanton's", "location": "Raleigh", "stock": 8},
        {"name": "Elijah Craig Barrel Proof", "location": "Cary", "stock": 5},
    ]

def save_inventory_to_csv(data, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "location", "stock"])
        writer.writeheader()
        writer.writerows(data)

def load_inventory_from_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def compare_inventories(old, new):
    old_set = {(item["name"], item["location"]) for item in old}
    new_set = {(item["name"], item["location"]) for item in new}
    added = new_set - old_set
    removed = old_set - new_set
    return list(added), list(removed)

def generate_delta_text(added, removed):
    lines = []
    if added:
        lines.append("📈 Items Added Since Last Report:")
        for name, location in added:
            lines.append(f"  - {name} at {location}")
    if removed:
        lines.append("\n📉 Items No Longer in Stock:")
        for name, location in removed:
            lines.append(f"  - {name} at {location}")
    if not added and not removed:
        lines.append("No inventory changes since the last report.")
    return "\n".join(lines)

def generate_inventory_text(data):
    lines = ["\n📦 Current Inventory:"]
    for item in data:
        lines.append(f"  - {item['name']} ({item['stock']} in stock at {item['location']})")
    return "\n".join(lines)

def save_txt(delta_text, inventory_text):
    with open(TXT_OUTPUT, "w") as f:
        f.write(delta_text + "\n\n" + inventory_text)

def save_html(delta_text, inventory_text):
    with open(HTML_OUTPUT, "w") as f:
        f.write("<html><body>")
        f.write("<h2>Delta Since Last Report</h2>")
        f.write(f"<pre>{delta_text}</pre>")
        f.write("<h2>Current Inventory</h2>")
        f.write(f"<pre>{inventory_text}</pre>")
        f.write("</body></html>")

def save_pdf(delta_text, inventory_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, delta_text + "\n\n" + inventory_text)
    pdf.output(PDF_OUTPUT)

def main():
    print("🔍 Running bourbon inventory search...")

    new_inventory = mock_bourbon_search()
    save_inventory_to_csv(new_inventory, CURRENT_CSV)

    old_inventory = load_inventory_from_csv(PREVIOUS_CSV)
    added, removed = compare_inventories(old_inventory, new_inventory)

    delta_text = generate_delta_text(added, removed)
    inventory_text = generate_inventory_text(new_inventory)

    save_txt(delta_text, inventory_text)
    save_html(delta_text, inventory_text)
    save_pdf(delta_text, inventory_text)

    os.replace(CURRENT_CSV, PREVIOUS_CSV)

    print("✅ Search complete. Results saved to:")
    print(f"- {TXT_OUTPUT}\n- {HTML_OUTPUT}\n- {PDF_OUTPUT}")

if __name__ == "__main__":
    main()

